import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

class LLMClassifier:
    def __init__(self):
        # We will try a few models in order of preference/stability
        self.output_model = 'models/gemini-2.5-flash'
        self.model = genai.GenerativeModel(self.output_model)

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
                response = self.model.generate_content(prompt)
                
                # Check for valid response
                if not response.text:
                    raise ValueError("Empty response from LLM")

                # Clean up the response to ensure it's valid JSON
                content = response.text.replace('```json', '').replace('```', '').strip()
                return json.loads(content)
            
            except Exception as e:
                print(f"LLM Error (Attempt {attempt + 1}): {e}")
                # If it's a rate limit (429), wait and retry
                if "429" in str(e) or "Resource exhausted" in str(e):
                    wait_time = 2 ** (attempt + 1) # 2, 4, 8 seconds
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    # If it's another error (like 404 model not found), maybe we should fail fast?
                    # But for now, let's just wait a bit and retry (or break if it's fatal)
                    # changing model dynamically is hard here without re-init.
                    break

        # Fallback if all retries fail
        return {
            "classification": "UNKNOWN",
            "risk_score": 0,
            "scam_type": "Analysis Failed",
            "red_flags": ["Could not verify with AI"],
            "advice": "Proceed with caution. The AI system is temporarily unavailable due to high traffic or limits."
        }
