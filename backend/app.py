import os
from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import random
import json
from flask_cors import CORS
from pathlib import Path
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for frontend-backend communication
CORS(app)

# Dynamically resolve paths for model and intents using pathlib
BASE_DIR = Path(__file__).resolve().parent
model_path = (BASE_DIR / "chatbotMODEL").resolve().as_posix()
intents_path = (BASE_DIR / "intents.json").resolve().as_posix()

# Debug: Log paths
logger.info(f"Model Path: {model_path}")
logger.info(f"Intents Path: {intents_path}")

# Load model and tokenizer
try:
    logger.info("Loading tokenizer...")
    tokenizer = BertTokenizer.from_pretrained(model_path)
    logger.info("Tokenizer loaded.")
    
    logger.info("Loading model...")
    model = BertForSequenceClassification.from_pretrained(model_path)
    logger.info("Model loaded.")
    
    logger.info("Initializing chatbot pipeline...")
    chatbot = pipeline("text-classification", model=model, tokenizer=tokenizer)
    logger.info("Chatbot pipeline initialized successfully.")
except Exception as e:
    logger.error(f"Error loading model/tokenizer: {e}")
    raise e

# Load intents
try:
    logger.info("Loading intents...")
    with open(intents_path, "r") as file:
        intents = json.load(file)
    logger.info("Intents loaded successfully.")
except Exception as e:
    logger.error(f"Error loading intents: {e}")
    raise e

def get_recommended_questions():
    """
    Function to get 5 recommended questions from specific tags in the intents file.
    """
    # Tags to pick from
    tags = [
        "hours", "number", "course", "fees", "location", "hostel", "event",
        "document", "syllabus", "library", "infrastructure", "canteen",
        "placement", "computerhod", "sem", "facilities", "committee",
        "vacation", "sports", "task"
    ]

    # Select 5 random tags
    selected_tags = random.sample(tags, 5)

    # Retrieve one random pattern (question) from each selected tag
    recommended_questions = []
    for tag in selected_tags:
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                question = random.choice(intent["patterns"])  # Pick one random question
                recommended_questions.append(question)
                break

    return recommended_questions

@app.route("/chat", methods=["POST"])
def chat():
    """
    Chatbot endpoint to handle user messages and return a response.
    """
    try:
        # Get user input from the frontend
        data = request.json
        user_input = data.get("message", "").strip()

        if not user_input:
            logger.warning("No message provided by the user.")
            return jsonify({"response": "No message provided.", "confidence": 0.0}), 400

        # Generate intent and score
        prediction = chatbot(user_input)[0]
        intent_label = prediction["label"]
        confidence = prediction["score"]

        logger.info(f"User Input: {user_input}")
        logger.info(f"Prediction: {prediction}")

        if confidence < 0.8:
            logger.info(f"Low confidence ({confidence}) for intent '{intent_label}'.")
            return jsonify({"response": "Sorry, I can't answer that right now.", "confidence": confidence})

        # Find the appropriate response for the intent
        for intent in intents["intents"]:
            if intent["tag"] == intent_label:
                response = random.choice(intent["responses"])
                logger.info(f"Responding with: {response}")
                return jsonify({"response": response, "confidence": confidence})

        # Fallback if intent not found
        logger.error(f"Intent '{intent_label}' not found in intents.")
        return jsonify({"response": "Sorry, something went wrong.", "confidence": confidence})

    except Exception as e:
        logger.error(f"Error in /chat endpoint: {e}")
        return jsonify({"response": "Internal server error.", "confidence": 0.0}), 500

@app.route("/recommended", methods=["GET"])
def recommended():
    """
    Endpoint to get 5 recommended questions for the user.
    """
    try:
        questions = get_recommended_questions()
        logger.info(f"Recommended Questions: {questions}")
        return jsonify({"recommended_questions": questions})
    except Exception as e:
        logger.error(f"Error in /recommended endpoint: {e}")
        return jsonify({"recommended_questions": [], "error": "Could not retrieve recommended questions."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
