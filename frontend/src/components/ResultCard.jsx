import React from 'react';

const ResultCard = ({ result }) => {
    if (!result) return null;

    const { classification, risk_score, scam_type, red_flags, advice } = result;

    const isScam = classification === 'SCAM';
    const isSuspicious = classification === 'SUSPICIOUS';

    let themeClass = 'theme-safe';
    if (isScam) themeClass = 'theme-scam';
    else if (isSuspicious) themeClass = 'theme-suspicious';

    // Calculate circle dasharray for progress (radius 45, circumference ~283)
    const radius = 45;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (risk_score / 100) * circumference;

    const handleShare = () => {
        const text = `⚠️ *Scam Alert Check* ⚠️\n\nI checked a message with Scam Detector AI:\n\n*Result:* ${classification}\n*Risk Score:* ${risk_score}/100\n*Type:* ${scam_type}\n\n*Advice:* ${advice}\n\nStay Safe!`;
        const url = `https://wa.me/?text=${encodeURIComponent(text)}`;
        window.open(url, '_blank');
    };

    return (
        <div className={`result-card ${themeClass}`}>
            <div className="result-header">
                <div className="classification">
                    <span className="badge">Classification</span>
                    <h2 className="text-main">{classification}</h2>
                    <p className="subtitle" style={{ margin: 0 }}>{scam_type}</p>
                </div>

                <div className="score-container">
                    <svg className="score-circle">
                        <circle cx="50" cy="50" r={radius} stroke="#334" strokeWidth="8" fill="transparent" />
                        <circle
                            cx="50" cy="50" r={radius}
                            stroke="currentColor"
                            strokeWidth="8"
                            fill="transparent"
                            className="progress-fill"
                            strokeDasharray={circumference}
                            strokeDashoffset={offset}
                            strokeLinecap="round"
                        />
                    </svg>
                    <div className="score-text text-main">
                        {risk_score}
                    </div>
                </div>
            </div>

            <div className="result-body">
                {/* Red Flags */}
                <div className="info-box red-flags">
                    <div className="info-title">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"></path>
                            <line x1="4" y1="22" x2="4" y2="15"></line>
                        </svg>
                        Detection Details
                    </div>
                    {red_flags.length > 0 ? (
                        <ul>
                            {red_flags.map((flag, index) => (
                                <li key={index}>
                                    <div className="flag-icon"></div>
                                    {flag}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="advice-text" style={{ fontStyle: 'italic' }}>No specific red flags found.</p>
                    )}
                </div>

                {/* Advice */}
                <div className="info-box advice">
                    <div className="info-title" style={{ color: '#2979ff' }}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="16" x2="12" y2="12"></line>
                            <line x1="12" y1="8" x2="12.01" y2="8"></line>
                        </svg>
                        Expert Advice
                    </div>
                    <p className="advice-text">
                        {advice}
                    </p>

                    <button onClick={handleShare} className="share-btn" style={{ marginTop: '1.5rem', background: '#25D366', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '8px', width: '100%', justifyContent: 'center' }}>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z" />
                        </svg>
                        Share Warning on WhatsApp
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ResultCard;
