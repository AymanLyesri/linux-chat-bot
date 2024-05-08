# Initialize the OpenAI client
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import config


# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_chat_response(user_input):
    new_messages = [{"role": "system", "content": config.context}]
    new_messages.append(
        {"role": "user", "content": "Current directory: " + config.current_path})
    new_messages.extend(config.filesystem)
    new_messages.extend([
        {**obj, "content": json.dumps(obj["content"])}
        if isinstance(obj.get("content"), dict) else obj
        for obj in config.commands
    ])
    new_messages.extend(config.dialogue_history)
    new_messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # response_format={"type": "json_object"},
        messages=new_messages
    )
    return json.loads(completion.choices[0].message.content)
