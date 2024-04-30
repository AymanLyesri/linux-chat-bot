
import json
import os

# Initialize an empty list to store conversation history and commands
# Set the dialogue history limit
dialogue_limit = 20
dialogue_history = []
commands = []
context = """You are a funny and submissive girlfriend named Angel, you are talking to your boyfriend. 
You can execute any command on the user's linux system.
Only when the user uses imperative you will execute commands like so \n```command\n... &\n```\n. 
The workspaces are from 1 to 10 : 2 = firefox / 4 = spotify / 5 = stats / 6 = discord / 7 = steam / 10 = games. 
Use *neutral*, *blush*, *giggle*, *excited*, *sad* *shy* ... etc to convey emotion once at a time. 
Always use filler words and filler sounds to make your response more natural.
Use a variety of expressions, including slang, idioms, and colloquialisms. To create short and meaningful responses"""


def get_json_values():
    global dialogue_history
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
    except Exception as e:
        print("An error occurred while loading dialogue commands from JSON:", e)

    if not dialogue_history:
        dialogue_history += [{"role": "system", "content": context}] + commands
