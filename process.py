import json
import re
import subprocess
import sys
import threading
import time
import config
import ai
import TTS


# Define a lock
speech_lock = threading.Lock()


def print_with_delay(message, delay=0.01):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


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


def process_input(user_input):
    response = ai.get_chat_response(user_input)
    # Print the bot's response
    # print_with_delay("\nWaifu: "+response)
    response_thread = threading.Thread(
        target=print_with_delay, args=("\nWaifu: "+response,))
    response_thread.start()

    # Append the user's input and bot's response to the dialogue history
    config.dialogue_history.extend([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response}])

    # Write dialogue_history to dialogue_history.log as JSON
    with open("dialogue_history.json", "w") as f:
        json.dump(config.dialogue_history, f, indent=4)

    # Check if the response contains an emotion
    path = "2/"
    image = "happy.jpg"
    expressions = extract_enclosed_word(response)
    if (len(expressions) > 0):
        if "giggle" in expressions[0]:
            image = "happy.jpg"
        elif "neutral" in expressions[0]:
            image = "neutral.jpg"
        elif "blush" in expressions[0]:
            image = "blush.jpg"
        elif "shy" in expressions[0]:
            image = "thinking.jpg"
        elif "excite" in expressions[0]:
            image = "excited.jpg"
        elif "sad" in expressions[0]:
            image = "sad.jpg"
    subprocess.run(["bash", "notification.sh", path+image,
                    remove_enclosed_words(response)])

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
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        if result.stderr and not result.stdout:
            print(f"\n\033[1;41m {result.stderr} \033[0m\n")
            process_input("I got an Error : " + result.stderr)
        if result.stdout and not result.stderr:
            # Assuming you want to limit to 10 lines
            limited_lines = result.stdout.split('\n')[:100]

            print('\n'.join(limited_lines))
            # config.dialogue_history.extend([
            #     {"role": "user", "content": result.stdout[:1000]},
            #     {"role": "assistant", "content": "I will remember this"}])
            process_input("Output : " + '\n'.join(limited_lines))
