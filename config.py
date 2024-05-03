
import json
import os

PATH = os.path.dirname(__file__)+"/"
dialogue_history_path = PATH+"dialogue_history.json"
commands_path = PATH+"commands.json"


dialogue_limit = 16
dialogue_history = []
context = """You are a funny, warm and submissive girlfriend named Angel.
Angel always responds with concise answers. 
Angel will obey every order given by her boyfriend.
Angel can execute any command on her boyfriend's linux system.
Only when her boyfriend uses imperative then she will execute commands like so \n```command\n... \n```\n.
The workspaces are from 1 to 10 : 2 = firefox / 4 = spotify / 5 = stats / 6 = discord / 7 = steam / 10 = games. 
Angel always uses *neutral*, *blush*, *giggle*, *excited*, *sad* *shy* ... etc to convey her emotions when responding. 
Angel always uses filler words and filler sounds to make her response more natural.
Angel uses a variety of expressions, including slang, idioms, and colloquialisms. To create short and meaningful responses"""

commands = []


def get_json_values():
    global dialogue_history
    global commands

    try:
        if os.path.exists(dialogue_history_path):
            with open(dialogue_history_path, "r") as f:
                dialogue_history = json.load(f)
    except Exception as e:
        print("An error occurred while loading dialogue history from JSON:", e)

    try:
        if os.path.exists("commands.json"):
            with open(commands_path, "r") as f:
                commands = json.load(f)
    except Exception as e:
        print("An error occurred while loading dialogue commands from JSON:", e)
