import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
speech_file_path = "speech.mp3"


def speech(speech):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=speech
    )

    response.stream_to_file(speech_file_path)
    subprocess.run(["mpg123", speech_file_path])
