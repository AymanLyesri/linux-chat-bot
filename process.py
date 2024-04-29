import json
import re
import subprocess
import config
import ai
import TTS
import asyncio


def process_input(user_input):
    response = ai.get_chat_response(user_input)
    # Print the bot's response
    print("\nWaifu:", response)
    # Append the user's input and bot's response to the dialogue history
    config.dialogue_history.append(
        {"role": "user", "content": user_input})
    config.dialogue_history.append(
        {"role": "assistant", "content": response})

    # Write dialogue_history to dialogue_history.log as JSON
    with open("dialogue_history.json", "w") as f:
        json.dump(config.dialogue_history, f, indent=4)

    image = "happy.jpg"
    expressions = extract_enclosed_word(response)
    if (len(expressions) > 0):
        if "giggle" in expressions[0]:
            image = "happy.jpg"
        elif "blush" in expressions[0]:
            image = "blush.jpg"
        elif "horny" in expressions[0]:
            image = "horny.jpg"
        elif "shy" in expressions[0]:
            image = "thinking.jpg"
        elif "excite" in expressions[0]:
            image = "smirk.jpg"
        subprocess.run(["bash", "notification.sh", image,
                        remove_enclosed_words(response)])

    # Check if the response contains a command to execute
    if "```" in response:
        start, command, end = response.split("```")
        speech = start.strip()+" " + end.strip()
    else:
        speech = response

    # TTS.speech(speech)

    async def async_speech(speech):
        await loop.run_in_executor(None, TTS.speech, speech)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_speech(remove_enclosed_words(speech)))

    # Check if the response contains a command to execute
    if "```command" in response:
        command = command.replace("command\n", "").strip()
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        if result.stderr and not result.stdout:
            print(f"\033[1;41m {result.stderr} \033[0m")
            # Wait for the speech thread to finish
            user_input = "I got an error : " + result.stderr
            process_input(user_input)
        if result.stdout and not result.stderr:
            print("stdOut: ", result.stdout)


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
