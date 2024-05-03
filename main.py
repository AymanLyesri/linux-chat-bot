
import json
import os
import sys
import config
import process


def get_input():
    # Get the size of the terminal
    rows, columns = os.popen('stty size', 'r').read().split()
    columns = int(columns)
    # Calculate the padding for the current_path
    left_padding = (columns - len(current_path)) // 2
    right_padding = columns - len(current_path) - left_padding
    # Create the = line with the current_path in the middle
    equal_line = "=" * left_padding + current_path + "=" * right_padding

    return input(
        "\n{}\n{}: ".format(equal_line, config.USER))


def main():
    global current_path
    if len(sys.argv) > 1:
        current_path = sys.argv[1]
    else:
        current_path = config.PATH
        instruction = "\n## Usage : python main.py <path> ##\n"
        hashtags = "#" * (len(instruction)-2)
        print(hashtags + instruction + hashtags)

    config.context += "\nCurrent directory is: " + current_path

    print("\nWelcome to Waifu chat bot!")
    print("You can start chatting by typing your messages.")
    print("Type 'forget' to forget the conversation.")

    while True:
        try:
            current_path = os.getcwd()
            if len(config.dialogue_history) > config.dialogue_limit:
                config.dialogue_history = config.dialogue_history[-config.dialogue_limit:]
                # Write dialogue_history to dialogue_history.log as JSON
                with open(config.dialogue_history_path, "w") as f:
                    json.dump(config.dialogue_history, f, indent=4)

            # refresh the json values
            config.get_json_values()

            user_input = get_input()

            # Check if the user wants to forget the conversation history
            if user_input.lower() == 'forget':
                config.dialogue_history = []
                process.process_input(
                    "Forget about what we talked about before")
                with open(config.dialogue_history_path, "w") as f:
                    json.dump([], f)
                config.get_json_values()

            # Check if the user wants to have normal conversation
            else:
                # Get the chatbot's response
                process.process_input(user_input)
        except KeyboardInterrupt or Exception:
            with open(config.PATH+'current_path.txt', 'w') as f:
                f.write(current_path)
            break


# main()
if __name__ == "__main__":
    main()
