import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    # Fallback to old key name just in case, or raise error
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY (or GEMINI_API_KEY) not found in environment variables")

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

class LLMClassifier:
    def __init__(self):
        # Use OpenRouter model ID
        self.output_model = 'google/gemini-2.0-flash-lite-001' 

    def analyze(self, text, url=None, ml_score=None):
        prompt = f"""
        You are an expert cybersecurity fraud and phishing detection system.

        Analyze the following website content and URL to determine if it is a scam, phishing page, fake job offer, financial fraud, or malicious site.

        Website URL:
        "{url if url else 'Not provided'}"

        Extracted Page Text (partial):
        "{text}"

        Consider these risk indicators:
        - Requests for OTP, passwords, or bank details
        - Urgent financial threats or account suspension warnings
        - Fake job offers asking for payment
        - Lottery or prize claims
        - Impersonation of banks, government, or brands
        - Suspicious domains or misspelled brand names
        - Requests to download unknown files
        - Pressure tactics ("Act now", "Limited time")

        Return ONLY valid JSON in this structure:

        {{
          "classification": "SCAM" or "SAFE" or "SUSPICIOUS",
          "risk_score": <0-100>,
          "scam_type": "Phishing, Job Scam, Fake Bank, Lottery Scam, etc.",
          "red_flags": ["string", "string"],
          "advice": "Clear safety advice for the user"
        }}

        Be strict. If financial or credential theft is possible, classify as SCAM.
        If uncertain but suspicious, mark as SUSPICIOUS.
        Do not include explanations outside JSON.
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Attempting analysis with {self.output_model} (Attempt {attempt + 1}/{max_retries})...")
                
                completion = client.chat.completions.create(
                    model=self.output_model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                response_text = completion.choices[0].message.content
                
                # Check for valid response
                if not response_text:
                    raise ValueError("Empty response from LLM")

                # Clean up the response to ensure it's valid JSON
                content = response_text.replace('```json', '').replace('```', '').strip()
                return json.loads(content)
            
            except Exception as e:
                with open("backend_errors.log", "a") as f:
                    f.write(f"LLM Error (Attempt {attempt + 1}): {e}\n")
                print(f"LLM Error (Attempt {attempt + 1}): {e}")
                
                # If it's a rate limit (429), wait and retry (OpenRouter might send 429 too)
                if "429" in str(e):
                    wait_time = 5 * (2 ** attempt) 
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    # Retry on other errors too for robustness, but maybe shorter wait?
                    time.sleep(2)
                    continue

        # Fallback if all retries fail
        return {
            "classification": "UNKNOWN",
            "risk_score": 0,
            "scam_type": "Analysis Failed",
            "red_flags": ["Could not verify with AI"],
            "advice": "Proceed with caution. The AI system is temporarily unavailable."
        }
