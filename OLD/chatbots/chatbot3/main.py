import random
import json
import subprocess
from difflib import SequenceMatcher
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Load the intents from the JSON file


def load_intents():
    with open('chatbots/chatbot3/intents.json') as file:
        return json.load(file)

# Save the updated intents to the JSON file


def save_intents(intents):
    with open('chatbots/chatbot3/intents.json', 'w') as file:
        json.dump(intents, file, indent=4)

# Function to get a response based on the input


def get_response(intents, input_text):
    max_similarity = 0
    closest_match = None
    input_tokens = [word for word in word_tokenize(
        input_text.lower()) if word not in stopwords.words('english')]
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern_tokens = [word for word in word_tokenize(
                pattern.lower()) if word not in stopwords.words('english')]
            similarity = SequenceMatcher(
                None, input_tokens, pattern_tokens).ratio()
            if similarity > max_similarity:
                max_similarity = similarity
                closest_match = intent
    if closest_match and max_similarity > 0.4:
        responses = closest_match['responses']
        if 'command' in closest_match:
            command = closest_match['command']
        else:
            command = None
        return random.choice(responses), command
    else:
        return None, None

# Function to mix responses to make them more human-like


def mix_responses(responses):
    mixed_response = ""
    for response in responses:
        mixed_response += random.choice(response) + " "
    return mixed_response.strip()

# Main function to interact with the chatbot


def chat():
    print("Start talking with the chatbot (type 'quit' to exit)!")
    intents = load_intents()
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response, command = get_response(intents, user_input)
        if response:
            if isinstance(response, list):
                response = mix_responses(response)
            subprocess.run(
                ['python', 'speech2.py', "{}".format(response), "&"])
            print("Bot:", response)

            if command:
                subprocess.run(command)
        else:
            apology = "I don't have a tag for that pattern."
            subprocess.run(
                ['python', 'speech2.py', apology])
            print("Bot: I don't have a tag for that pattern.")


# Run the chat function
chat()
