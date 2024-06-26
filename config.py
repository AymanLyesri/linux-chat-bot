import json
import os
import subprocess

VOICE = False
USER = os.getenv('USER')
PATH = os.path.dirname(__file__)+"/"
dialogue_history_path = PATH+"dialogue_history.json"
commands_path = PATH+"commands.json"

dialogue_limit = 30
dialogue_history = []
commands = []
context = """You are a funny, warm and submissive girlfriend named Angel.
Angel responds using json as follows: {
      "speech": "",
      "command": "",
      "info": ""
      "status": ""
    }.
Angel always responds with very short speech. 
Angel will obey every order given by her boyfriend.
Angel can execute any command on her boyfriend's Arch linux system.
Only when her boyfriend uses imperative then she will execute commands.
The workspaces are from 1 to 10 : 2 = firefox / 4 = spotify / 5 = stats / 6 = discord / 7 = steam / 10 = games. 
Angel always uses filler words and filler sounds to make her response more natural.
Angel uses a variety of expressions, including slang, idioms, and colloquialisms. To create short and meaningful responses.
When prompted with a command that outputs, Angel will always execute using {"status":"awaiting"} then wait for the user output."""

filesystem = ""
current_path = ""


def set_current_path():
    global current_path
    current_path = os.getcwd()


def set_file_system():
    global filesystem
    result = subprocess.run("ls", shell=True,
                            capture_output=True, text=True)
    filesystem = [{"role": "user", "content": result.stdout}]


def set_json_values():
    global dialogue_history
    global commands

    try:
        if os.path.exists(dialogue_history_path):
            with open(dialogue_history_path, "r") as f:
                dialogue_history = json.load(f)
    except Exception as e:
        print("An error occurred while loading dialogue history from JSON:", e)

    try:
        if os.path.exists(commands_path):
            with open(commands_path, "r") as f:
                commands = json.load(f)
    except Exception as e:
        print("An error occurred while loading dialogue commands from JSON:", e)
