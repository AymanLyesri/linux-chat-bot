# Initialize the OpenAI client
import os
from dotenv import load_dotenv
from openai import OpenAI
import config

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_chat_response(user_input):
    # Generate a chatbot response
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=config.dialogue_history + [
            {"role": "user", "content": user_input}
        ]
    )
    return completion.choices[0].message.content
