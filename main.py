
import json
import os
import config
import process


def get_input():
    # Get the size of the terminal
    rows, columns = os.popen('stty size', 'r').read().split()
    columns = int(columns)
    # Calculate the padding for the config.current_path
    left_padding = (columns - len(config.current_path)) // 2
    right_padding = columns - len(config.current_path) - left_padding
    # Create the = line with the config.current_path in the middle
    equal_line = "=" * left_padding + config.current_path + "=" * right_padding

    return input(
        "\n{}\n{}: ".format(equal_line, config.USER.capitalize()))


def main():

    print("\nWelcome to Angel chat bot!")
    print("You can start chatting by typing your messages.")
    print("Type 'forget' to forget the conversation.")

    while True:
        try:
            if len(config.dialogue_history) > config.dialogue_limit:
                config.dialogue_history = config.dialogue_history[-config.dialogue_limit:]
                # Write dialogue_history to dialogue_history.log as JSON
                with open(config.dialogue_history_path, "w") as f:
                    json.dump(config.dialogue_history, f, indent=4)

            # refresh the json values
            config.set_json_values()
            config.set_file_system()
            config.set_current_path()

            user_input = get_input()

            # Check if the user wants to forget the conversation history
            if user_input.lower() == 'forget':
                config.dialogue_history = []
                process.process_input(
                    "Forget about what we talked about before")
                with open(config.dialogue_history_path, "w") as f:
                    json.dump([], f)
                config.set_json_values()
            # Check if the user wants to have normal conversation
            else:
                process.process_input(user_input)
        except Exception:
            with open(config.PATH+'config.current_path.txt', 'w') as f:
                f.write(config.current_path)
            break


# main()
if __name__ == "__main__":
    main()
