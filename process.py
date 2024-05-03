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
import TTS2
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


# execute command
def executeCommand(command, print_output=True):
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
            result = subprocess.run(command, shell=True,
                                    capture_output=True, text=True)
            if result.stderr and not result.stdout:
                print(f"\n\033[1;41m {result.stderr} \033[0m")
                addToHistory(input=result.stderr)
            if result.stdout and not result.stderr:
                limited_lines = result.stdout.split('\n')[:200]
                if print_output:
                    print('\n'.join(limited_lines))
                addToHistory(input='\n'.join(limited_lines))
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
        target=print_with_delay, args=("\nWaifu: "+response,))
    response_thread.start()

    addToHistory(user_input, response)

    notification.send_notification(response)

    # Acquire the lock before starting the speech_thread
    with speech_lock:
        # Use regular expressions to find all occurrences of "```command <command>```" in the sentence
        speech = re.sub(r"```command\n([^`]+)```", "", response)
        speech = speech.replace("\n", " ").strip()
        speech = remove_enclosed_words(speech)
        if speech != "":
            speech_thread = threading.Thread(
                target=TTS.speech, args=(speech,))
            # Wait for the previous speech_thread to finish
            if speech_thread is not None and speech_thread.is_alive():
                print("Waiting for the previous speech to finish...")
                speech_thread.join()
            # Create a new thread to play the speech
            speech_thread.start()

    # Wait for the waifu response thread to finish
    response_thread.join()

    # Check if the response contains a command to execute
    if "```command" in response:
        commands = re.findall(
            r"```command\n([^`]+)```", response.replace("\\`", ""))
        commands_array = [command.strip() for command in commands]

        for command in commands_array:
            if "&&" in command:
                # If "&&" is present, split the command string based on it
                for command in command.split(" && "):
                    executeCommand(command)
            else:
                executeCommand(command)
