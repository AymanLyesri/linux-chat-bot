import os
import shlex

path = "2"


def extract_enclosed_word(text):
    # Split the text by asterisks
    parts = text.split('*')

    # Filter out parts that are enclosed by asterisks
    enclosed_words = [part.strip()
                      for i, part in enumerate(parts) if i % 2 == 1]

    return enclosed_words


def send_notification(notification_message):
    # Check if the response contains an emotion
    image = "happy.jpg"
    expressions = extract_enclosed_word(notification_message)
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
    # Send the notification using notify-send
    icon_path = os.path.expanduser(
        "~/python_chat_bot/expressions/{}/{}".format(path, image))

    # Construct the command with proper escaping
    command = "notify-send -i {} {}".format(
        shlex.quote(icon_path), shlex.quote(notification_message))

    # Execute the command
    os.system(command)
