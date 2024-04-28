import json
import re
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

context = "You are a playful and horny girlfriend. You are talking to your boyfriend. Always Using blush, giggle, exited, horny, shy, wink etc to convey your emotions."

# Set the dialogue history limit
dialogue_limit = 30


def get_chat_response(user_input, dialogue_history):
    # Generate a chatbot response
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=dialogue_history + [
            {"role": "user", "content": user_input}
        ]
    )
    return completion.choices[0].message.content


def processResponse(response):
    expressions = extract_enclosed_word(response)
    print(expressions)
    for expression in expressions:
        print(expression)
        image = "horny.jpg"
        if "giggle" in expression:
            image = "happy.jpg"
        elif "blush" in expression:
            image = "blush.jpg"
        elif "horny" in expression:
            image = "horny.jpg"
        elif "shy" in expression:
            image = "thinking.jpg"
    # Display the image notification
        subprocess.run(["bash", "notification.sh", image,
                       remove_enclosed_words(response), "&"])
    speech = response.split("|")[0]
    if "|" in response:
        bash = response.split("|")[1]
        subprocess.run(bash, shell=True, capture_output=True, text=True)

    # Play the bot's response as speech
    subprocess.run(["python", "speech.py", remove_enclosed_words(speech)])


def extract_enclosed_word(text):
    # Split the text by asterisks
    parts = text.split('*')

    # Filter out parts that are enclosed by asterisks
    enclosed_words = [part.strip()
                      for i, part in enumerate(parts) if i % 2 == 1]

    return enclosed_words


def remove_enclosed_words(text):
    # Define a regular expression pattern to match words enclosed in asterisks
    pattern = r'\*([^*]+)\*'

    # Use sub() function to replace matched patterns with an empty string
    result = re.sub(pattern, '', text)

    return result.strip()


def main():

    # Initialize an empty list to store conversation history
    dialogue_history = []

    try:
        if os.path.exists("dialogue_history.json"):
            with open("dialogue_history.json", "r") as f:
                loaded_history = json.load(f)
                if loaded_history:
                    dialogue_history += loaded_history
    except Exception as e:
        print("An error occurred while loading dialogue history from JSON:", e)

    try:
        if os.path.exists("commands.json"):
            with open("commands.json", "r") as f:
                commands = json.load(f)
                if commands:
                    dialogue_history += commands
    except Exception as e:
        print("An error occurred while loading dialogue commands from JSON:", e)

    # If the dialogue history is empty, add the context
    if not dialogue_history:
        dialogue_history.append(
            {"role": "system", "content": context})
    # If the dialogue history is not empty, add the context as the first item
    else:
        dialogue_history[0] = {"role": "system", "content": context}

    print("Welcome to Simple ChatBot!")
    print("You can start chatting by typing your messages.")
    print("Type 'exit' to end the conversation.")

    while True:

        # Check if the dialogue history exceeds 10 items, remove the oldest conversations
        if len(dialogue_history) > dialogue_limit:
            dialogue_history = dialogue_history[-dialogue_limit:]

        # If the dialogue history is empty, add the context
        if not dialogue_history:
            dialogue_history.append(
                {"role": "system", "content": context})
        # If the dialogue history is not empty, add the context as the first item
        else:
            dialogue_history[0] = {"role": "system", "content": context}

        # Get user input
        user_input = input("You: ")

        # Get the chatbot's response
        response = get_chat_response(user_input, dialogue_history)
        print("Bot:", response)

        # Process the bot's response
        processResponse(response)

        # Append the user's input and bot's response to the dialogue history
        dialogue_history.append({"role": "user", "content": user_input})
        dialogue_history.append({"role": "assistant", "content": response})

        # Write dialogue_history to dialogue_history.log as JSON
        with open("dialogue_history.json", "w") as f:
            json.dump(dialogue_history, f, indent=4)

        # Check if the user wants to exit the conversation
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'forget':
            dialogue_history = []
            with open("dialogue_history.json", "w") as f:
                json.dump([], f)


if __name__ == "__main__":
    main()
