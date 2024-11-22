import axios from "axios";

// Define the API base URL
const BASE_URL = "http://localhost:5000"; // Replace with your backend server URL if hosted remotely

// Function to send a message to the backend
export const sendMessage = async (message) => {
  try {
    // Send a POST request to the backend chat endpoint
    const response = await axios.post(`${BASE_URL}/chat`, {
      message: message,
    });

    // Return the bot's response
    return {
      sender: "bot",
      text: response.data.response, // The bot's reply from the backend
    };
  } catch (error) {
    console.error("Error while sending message to the chatbot:", error);

    // Fallback message in case of an error
    return {
      sender: "bot",
      text: "Sorry, I encountered an error. Please try again later.",
    };
  }
};

// Function to get recommended questions from the backend
export const getRecommendedQuestions = async () => {
  try {
    // Send a GET request to the backend recommended endpoint
    const response = await axios.get(`${BASE_URL}/recommended`);

    // Return the recommended questions
    return response.data.recommended_questions;
  } catch (error) {
    console.error("Error while fetching recommended questions:", error);

    // Fallback message in case of an error
    return [
      "Sorry, I couldn't fetch recommended questions at the moment.",
    ];
  }
};
