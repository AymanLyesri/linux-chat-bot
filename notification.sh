#!/bin/bash

# Check if the script is called with an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <notification_message>"
    exit 1
fi

# Extract the argument (notification message)
notification_image="$1"
notification_message="$2"

# Send the notification using notify-send
notify-send -i ~/python_chat_bot/expressions/"$notification_image" "$notification_message"
