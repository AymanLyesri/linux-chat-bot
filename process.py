import json
import os
import re
import subprocess
import sys
import threading
import time
import config
import ai
import TTS
import notification


# Define a lock
speech_lock = threading.Lock()

# This is the flag we'll use to signal the thread to stop
stop_thread = threading.Event()


def loading_animation():
    animation_chars = ['-', '\\', '|', '/']  # Define animation characters
    while not stop_thread.is_set():
        for char in animation_chars:
            sys.stdout.write('\r'+char)
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\r ')
    sys.stdout.flush()


def print_with_delay(message, delay=0.01):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def remove_enclosed_words(text):
    pattern = r'\*([^*]+)\*'
    result = re.sub(pattern, '', text)
    return result.strip()


def addToHistory(input=None, output=None):
    if input:
        config.dialogue_history.extend([{"role": "user", "content": input}])
    if output:
        config.dialogue_history.extend(
            [{"role": "assistant", "content": output}])

    # Write dialogue_history to dialogue_history.log as JSON
    with open(config.dialogue_history_path, "w") as f:
        json.dump(config.dialogue_history, f, indent=4)


def switchVoice():
    config.VOICE = True


# execute command
def executeCommand(command, print_output=True):
    if command == "switchVoice()":
        switchVoice()
        return
    try:
        if "cd" in command:
            try:
                # remove cd from command
                path = command.replace("cd ", "").strip()
                path = os.path.expanduser(path)
                os.chdir(path)
            except Exception as e:
                print(f"An error HAS occurred while cd: {e}")
        else:
            try:
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=5)
            except subprocess.TimeoutExpired:
                print("The command did not complete within 5 seconds.")
                return "Command timed out"
            if result.stderr and not result.stdout:
                print(f"\n\033[1;41m {result.stderr} \033[0m")
                addToHistory(input=result.stderr)
            if result.stdout and not result.stderr:
                # limited_lines = result.stdout.split('\n')[:200]
                if print_output:
                    print("------output: ", result.stdout)
                return result.stdout
    except Exception as e:
        addToHistory(e, "Do you want me to fix it?")
        print(f"An error HAS occurred while executing command: {e}")


def process_input(user_input):
    # Loading animation
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    response = ai.get_chat_response(user_input)

    # Signal the loading animation to stop
    stop_thread.set()
    # Wait for the loading animation to finish
    loading_thread.join()
    # Clear the stop_thread event for the next loading animation
    stop_thread.clear()

    # print_with_delay("\nWaifu: "+response)
    response_thread = threading.Thread(
        target=print_with_delay, args=("\nWaifu: " + human_readable(response),))
    response_thread.start()

    addToHistory(user_input, json.dumps(response))

    notification.send_notification(response["speech"])

    # Acquire the lock before starting the speech_thread
    with speech_lock:
        # Use regular expressions to find all occurrences of "```command <command>```" in the sentence
        if response["speech"] != "" and config.VOICE:
            speech_thread = threading.Thread(
                target=TTS.speech, args=(response["speech"],))
            # Wait for the previous speech_thread to finish
            if speech_thread is not None and speech_thread.is_alive():
                print("Waiting for the previous speech to finish...")
                speech_thread.join()
            # Create a new thread to play the speech
            speech_thread.start()

    # Wait for the waifu response thread to finish
    response_thread.join()

    # Check if the response contains a command to execute
    if response["command"]:
        if "&&" in response["command"]:
            # If "&&" is present, split the command string based on it
            for command in response["command"].split(" && "):
                output = executeCommand(command)
                if output and response["status"] == "awaiting":
                    process_input("OUTPUT: " + output)
                else:
                    addToHistory(input=output)
        else:
            output = executeCommand(response["command"])
            if output and response["status"] == "awaiting":
                process_input("OUTPUT: " + output)
            else:
                addToHistory(input=output)


def human_readable(json):
    output = json["speech"]
    if json["command"]:
        output += "\n---Command: {}\n".format(json["command"])
    if json["info"]:
        output += "\n---Info: {}\n".format(json["info"])
    return output
