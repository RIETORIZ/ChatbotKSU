import random
import json
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
# Paths to the model and intents.json
model_path = r"C:\ChatBotProject\backend\chatbotBE\chatbotMODEL"
intents_path = r"C:\ChatBotProject\backend\chatbotBE\intents.json"
# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

# Define the chatbot pipeline
chatbot = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Load intents.json
with open(intents_path, "r") as file:
    intents = json.load(file)

# Map labels to intents index (Ensure this matches your trained labels)
label2id = {label: index for index, label in enumerate(intent['tag'] for intent in intents['intents'])}
def chat(chatbot):
    print("Chatbot: Hi! I am your virtual assistant. Feel free to ask, and I'll do my best to provide answers and assistance.")
    print("Type 'quit' to exit the chat\n\n")

    # Get user input
    text = input("User: ").strip().lower()

    while text != 'quit':
        # Get prediction and score
        prediction = chatbot(text)[0]
        label = prediction['label']
        score = prediction['score']

        if score < 0.8:
            print("Chatbot: Sorry, I can't answer that.\n\n")
        else:
            # Get intent index and random response
            intent_index = label2id[label]
            response = random.choice(intents['intents'][intent_index]['responses'])
            print(f"Chatbot: {response}\n\n")

        # Get next input
        text = input("User: ").strip().lower()
if __name__ == "__main__":
    chat(chatbot)
