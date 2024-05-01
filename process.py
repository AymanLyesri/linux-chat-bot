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


def print_with_delay(message, delay=0.01):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def remove_enclosed_words(text):
    # Define a regular expression pattern to match words enclosed in asterisks
    pattern = r'\*([^*]+)\*'

    # Use sub() function to replace matched patterns with an empty string
    result = re.sub(pattern, '', text)

    return result.strip()


def addToHistory(user_input, response):
    # Append the user's input and bot's response to the dialogue history
    config.dialogue_history.extend([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response}])

    # Write dialogue_history to dialogue_history.log as JSON
    with open("dialogue_history.json", "w") as f:
        json.dump(config.dialogue_history, f, indent=4)


def process_input(user_input):
    response = ai.get_chat_response(user_input)
    # Print the bot's response
    # print_with_delay("\nWaifu: "+response)
    response_thread = threading.Thread(
        target=print_with_delay, args=("\nWaifu: "+response,))
    response_thread.start()

    addToHistory(user_input, response)

    notification.send_notification(response)

    # Check if the response contains a command to execute
    if "```" in response:
        start, command, end = response.split("```")
        speech = remove_enclosed_words(start.strip()+" " + end.strip())
    else:
        speech = remove_enclosed_words(response)

    # Acquire the lock before starting the speech_thread
    with speech_lock:
        if speech != "":
            speech_thread = threading.Thread(
                target=TTS.speech, args=(speech,))
            # Wait for the previous speech_thread to finish
            if speech_thread.is_alive():
                print("Waiting for the previous speech to finish...")
                speech_thread.join()
            # Create a new thread to play the speech
            speech_thread.start()

    # Wait for the waifu response thread to finish
    response_thread.join()

    # Check if the response contains a command to execute
    if "```command" in response:
        command = command.replace("command\n", "").strip()
        if "cd" in command:
            # remove cd from command
            path = command.replace("cd", "").strip()
            os.chdir(path)
        else:
            result = subprocess.run(command, shell=True,
                                    capture_output=True, text=True)
            if result.stderr and not result.stdout:
                print(f"\n\033[1;41m {result.stderr} \033[0m\n")
                addToHistory(result.stderr, "Do you want me to fix it?")
            if result.stdout and not result.stderr:
                # Assuming you want to limit to 10 lines
                limited_lines = result.stdout.split('\n')[:100]
                print('\n'.join(limited_lines))
                addToHistory('\n'.join(limited_lines),
                             "I will keep this in mind")
