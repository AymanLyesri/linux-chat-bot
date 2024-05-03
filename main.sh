#!/bin/bash

MAIN_CHAT_BOT_DIR="/home/ayman/linux-chat-bot"

source $MAIN_CHAT_BOT_DIR/activate.sh && python $MAIN_CHAT_BOT_DIR/main.py $1 && cd $(cat $MAIN_CHAT_BOT_DIR/current_path.txt)
CURRENT_FOLDER=$(basename "$PWD")
