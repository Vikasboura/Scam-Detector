import React, { useState } from 'react';
import axios from 'axios';
import ResultCard from './components/ResultCard';

const App = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleScanPage = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Get current tab
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

      if (!tab) {
        throw new Error("No active tab found");
      }

      // Execute script to get page text
      const injectionResults = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => document.body.innerText,
      });

      const pageText = injectionResults[0].result;
      const url = tab.url;

      // Send to backend
      // Send to backend
      const apiUrl = 'https://scam-detector-1-9wqs.onrender.com';
      const response = await axios.post(`${apiUrl}/analyze`, {
        message: pageText.substring(0, 5000), // Limit text length
        url: url
      });

      setResult(response.data);
    } catch (err) {
      console.error(err);
      const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
      setError(`Failed to analyze page: ${errorMessage}. Ensure backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <div className="shine-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
          </svg>
        </div>
        <h1 className="title">Scam Detector</h1>
        <p className="subtitle">
          Scan current page for risks
        </p>
      </div>

      <div className="analysis-card" style={{ textAlign: 'center' }}>
        <button
          onClick={handleScanPage}
          disabled={loading}
          className="analyze-btn"
        >
          {loading ? (
            <>
              <div className="spinner"></div>
              Scanning...
            </>
          ) : (
            <>
              Scan This Page
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" width="20" height="20">
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {result && <ResultCard result={result} />}
    </div>
  );
};

export default App;
