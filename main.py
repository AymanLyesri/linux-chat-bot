
import json
import sys
import config
import process


def main():

    print(sys.argv[1])
    print("Welcome to Simple ChatBot!")
    print("You can start chatting by typing your messages.")
    print("Type 'exit' to end the conversation.")

    while True:
        try:
            if len(config.dialogue_history) > config.dialogue_limit:
                config.dialogue_history = config.dialogue_history[-config.dialogue_limit:]
                # Write dialogue_history to dialogue_history.log as JSON
                with open(config.dialogue_history_path, "w") as f:
                    json.dump(config.dialogue_history, f, indent=4)

            config.get_json_values()

            # Get user input
            user_input = input(
                "\n===============================================\nYou: ")

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
        except KeyboardInterrupt:
            # process.process_input("Goodbye")
            break


# main()
if __name__ == "__main__":
    main()
