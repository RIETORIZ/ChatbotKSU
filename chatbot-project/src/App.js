import React, { useEffect, useState } from 'react';
import './App.css';
import Sidebar from './Sidebar';
import { getRecommendedQuestions, sendMessage } from './api';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [userPic, setUserPic] = useState('boy'); // Default user avatar
  const [recommendedQuestions, setRecommendedQuestions] = useState([]);

  useEffect(() => {
    const root = document.documentElement;
    root.className = 'dark-mode'; // Force dark theme
    fetchRecommendedQuestions(); // Fetch initial recommended questions
  }, []);

  const fetchRecommendedQuestions = async () => {
    const questions = await getRecommendedQuestions();
    setRecommendedQuestions(questions);
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);

    try {
      const botResponse = await sendMessage(input);
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    } catch (error) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: 'Sorry, something went wrong!' },
      ]);
    }

    setInput('');
  };

  const handleRecommendedClick = async (index) => {
    const newQuestion = (await getRecommendedQuestions())[0]; // Fetch a new question
    setRecommendedQuestions((prevQuestions) => {
      const updatedQuestions = [...prevQuestions];
      updatedQuestions[index] = newQuestion; // Replace only the clicked question
      return updatedQuestions;
    });
    setInput(recommendedQuestions[index]); // Set the clicked question in the input field
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="chat-container">
      <Sidebar
        setUserPic={setUserPic}
        recommendedQuestions={recommendedQuestions}
        handleRecommendedClick={handleRecommendedClick}
      />
      <div className="chat-main">
        <div className="chat-header">
          <img
            src="/favicon.ico"
            alt="Chat Icon"
            style={{ width: 60, height: 60, marginLeft: 10 }}
          />
          KSUChatbot
        </div>
        <div className="chat-body">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <img
                src={msg.sender === 'user' ? `/${userPic}.png` : '/KSUbot.png'}
                alt={`${msg.sender} avatar`}
                style={{ width: 30, height: 30, marginRight: 10 }}
              />
              <span>{msg.text}</span>
            </div>
          ))}
        </div>
        <div className="chat-footer">
          <input
            type="text"
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress} // Add "Enter" key support
            placeholder="Type your message..."
          />
          <button className="chat-button" onClick={handleSendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;
