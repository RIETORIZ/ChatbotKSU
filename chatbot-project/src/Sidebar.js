import React from 'react';
import './App.css';

const Sidebar = ({ setUserPic, recommendedQuestions, handleRecommendedClick }) => {
  return (
    <div className="sidebar">
      <div>
        <div className="sidebar-header">
          <img
            src="/KSUbot.png"
            alt="Bot Icon"
            style={{ width: 60, height: 60, marginLeft: 10 }}
          />
          KSUChatbot
        </div>
        <h3>Choose Your Avatar</h3>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          <img
            src="/boy.png"
            alt="Boy Avatar"
            style={{ width: 50, height: 50, cursor: 'pointer' }}
            onClick={() => setUserPic('boy')}
          />
          <img
            src="/girl.png"
            alt="Girl Avatar"
            style={{ width: 50, height: 50, cursor: 'pointer' }}
            onClick={() => setUserPic('girl')}
          />
          <img
            src="/KSUbot.png"
            alt="Bot Avatar"
            style={{ width: 50, height: 50, cursor: 'pointer' }}
            onClick={() => setUserPic('bot')}
          />
        </div>
        <h3>Recommended Questions</h3>
        <div className="recommended-questions">
          {recommendedQuestions.map((question, index) => (
            <button
              key={index}
              className="chat-button"
              style={{
                display: 'block',
                marginBottom: '10px',
                width: '100%', // Make buttons take full width
              }}
              onClick={() => handleRecommendedClick(index)}
            >
              {question}
            </button>
          ))}
        </div>
      </div>
      <div>
        <h3>About</h3>
        <p>
          This chatbot simulates responses to user queries. It can assist with FAQs,
          provide information, and simulate conversational AI for testing purposes.
        </p>
      </div>
    </div>
  );
};

export default Sidebar;
