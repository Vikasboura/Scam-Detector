# 🛡️ AI Scam Detection System

**Protect yourself from online fraud with the power of Artificial Intelligence.**

This project is a full-stack **AI-powered Scam Detector** that analyzes web pages and text messages to identify potential risks. It combines traditional Machine Learning (ML) with advanced Large Language Models (LLMs) to provide detailed risk assessments.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![React](https://img.shields.io/badge/react-v18+-61DAFB.svg)

## ✨ Features

*   **Real-time Analysis**: Scans web page content instantly using a Chrome Extension.
*   **Dual-Engine Detection**:
    *   **ML Engine**: Fast spam/ham classification using Scikit-Learn.
    *   **LLM Engine**: Deep contextual analysis using Google Gemini AI to catch subtle scams.
*   **Risk Scoring**: Provides a clear 0-100 risk score with a "Safe", "Suspicious", or "High Risk" verdict.
*   **Detailed Insights**: Explains *why* a page is dangerous (e.g., "Urgency", "Request for Sensitive Data").
*   **WhatsApp Integration**: (Optional) Analyze messages via a WhatsApp bot.
*   **Demo Video**: [Watch Demo](#demo-video)

## 🎥 Demo Video

<video src="demo video/compressed-video.mp4" controls="controls" style="max-width: 100%;">
</video>

[Download/Watch Video File](demo%20video/compressed-video.mp4)

> **Note**: If the video doesn't play directly above, click the link to view it.

## 🚀 Tech Stack

*   **Frontend**: React, Vite, Tailwind CSS
*   **Backend**: Python, FastAPI
*   **AI/ML**: Scikit-Learn (Random Forest), Google Gemini API
*   **Deployment**: Render (Backend),vercel (frontend), Chrome Web Store (Extension)

## 🛠️ Installation & Setup

### Prerequisites
*   Node.js & npm
*   Python 3.9+
*   Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/Vikasboura/scam-detector.git
cd scam-detector
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Create .env file with your API Key
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

## 🏃‍♂️ Running Locally

You can run the entire project with the included script (Windows):
```powershell
.\start_app.ps1
```
Or manually:
*   **Backend**: `uvicorn main:app --reload` (Port 8000)
*   **Frontend**: `npm run dev` (Port 5173)

## 🧩 Chrome Extension Usage

To use this as a browser extension:

1.  **Build the Frontend**:
    ```bash
    cd frontend
    npm run build
    ```
2.  **Load in Chrome**:
    *   Go to `chrome://extensions`
    *   Enable **Developer Mode** (top right).
    *   Click **Load unpacked**.
    *   Select `scam-detector/frontend/dist`.
3.  **Scan**: Open any webpage, click the extension icon, and hit "Scan This Page".

## ☁️ Deployment

*   **Backend**: Ready for **Render** (includes `Procfile`).
*   **Frontend**: Ready for **Vercel** code (includes `vercel.json`).
