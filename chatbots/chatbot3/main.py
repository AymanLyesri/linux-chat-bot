import random
import json
import subprocess
import difflib

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
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            similarity = difflib.SequenceMatcher(
                None, input_text.lower(), pattern.lower()).ratio()
            if similarity > max_similarity:
                max_similarity = similarity
                closest_match = intent
    # print(closest_match, max_similarity)
    if closest_match and max_similarity > 0.5:
        if 'command' in closest_match:
            return random.choice(closest_match['responses']), closest_match['command']
        else:
            return random.choice(closest_match['responses']), None
    else:
        return None, None

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
            print("Bot:", response)
            subprocess.run(["notify-send", "{}".format(response)])
            subprocess.run(['python', 'speech.py', "{}".format(response), "&"])
            if command:
                subprocess.run(command)
        else:
            print("Bot: Can you provide a response for that?")
            new_response = input("You: ")
            tag = None
            for intent in intents['intents']:
                for pattern in intent['responses']:
                    if new_response.lower() == pattern.lower():
                        tag = intent['tag']
                        for intent in intents['intents']:
                            if intent['tag'] == tag:
                                intent['patterns'].append(user_input)
                                save_intents(intents)
                                print("Bot: Thanks! I've learned from that.")
                                break
                if tag:
                    break
            else:
                print("Bot: I don't have a tag for that pattern.")


# Run the chat function
chat()
