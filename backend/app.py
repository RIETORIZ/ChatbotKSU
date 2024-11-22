from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import random
import json
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for frontend-backend communication
CORS(app)

# Paths for model and intents
model_path = "C:/ChatBotProject/backend/chatbotBE/chatbotMODEL"
intents_path = "C:/ChatBotProject/backend/chatbotBE/intents.json"

# Load model and tokenizer
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
chatbot = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Load intents
with open(intents_path, "r") as file:
    intents = json.load(file)


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
    # Get user input from the frontend
    data = request.json
    user_input = data.get("message", "")

    # Generate intent and score
    prediction = chatbot(user_input)[0]
    intent_label = prediction["label"]
    confidence = prediction["score"]

    if confidence < 0.8:
        return jsonify({"response": "Sorry, I can't answer that right now.", "confidence": confidence})

    # Find the appropriate response for the intent
    for intent in intents["intents"]:
        if intent["tag"] == intent_label:
            response = random.choice(intent["responses"])
            return jsonify({"response": response, "confidence": confidence})

    # Fallback if intent not found
    return jsonify({"response": "Sorry, something went wrong.", "confidence": confidence})


@app.route("/recommended", methods=["GET"])
def recommended():
    """
    Endpoint to get 5 recommended questions for the user.
    """
    questions = get_recommended_questions()
    return jsonify({"recommended_questions": questions})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
