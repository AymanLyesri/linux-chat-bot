
import json
import config
import process


def main():

    config.get_json_values()

    print("Welcome to Simple ChatBot!")
    print("You can start chatting by typing your messages.")
    print("Type 'exit' to end the conversation.")

    while True:

        # Check if the dialogue history exceeds 10 items, remove the oldest conversations
        if len(config.dialogue_history) > config.dialogue_limit:
            config.dialogue_history = config.dialogue_history[-config.dialogue_limit:]

        # If the dialogue history is empty, add the context
        if not config.dialogue_history:
            config.dialogue_history.append(
                {"role": "system", "content": config.context})
        # If the dialogue history is not empty, add the context as the first item
        else:
            config.dialogue_history[0] = {
                "role": "system", "content": config.context}

        # Get user input
        user_input = input(
            "\n===============================================\nYou: ")

        # Check if the user wants to exit the conversation
        if user_input.lower() == 'exit':
            process.process_input("Goodbye")
            break
        # Check if the user wants to forget the conversation history
        elif user_input.lower() == 'forget':
            config.dialogue_history = []
            process.process_input("Forget about what we talked about before")
            with open("dialogue_history.json", "w") as f:
                json.dump([], f)
            config.get_json_values()

        # Check if the user wants to have normal conversation
        else:
            # Get the chatbot's response
            process.process_input(user_input)


# main()
if __name__ == "__main__":
    main()
