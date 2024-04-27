import subprocess
import sys
import requests
import base64
import io
from pydub import AudioSegment
from pydub.playback import play

url = 'https://tts-tiktok.p.rapidapi.com/tts/v1/tts-tiktok-1'
headers = {
    'content-type': 'application/json',
    'X-RapidAPI-Key': 'eda5c736e8msha192a972ef3bc0bp175619jsn8694b5f19f74',
    'X-RapidAPI-Host': 'tts-tiktok.p.rapidapi.com'
}
params = {
    'response': 'base64'
}
data = {
    'lang': 'english_us',
    'voice': 'female_1',
    'text': sys.argv[1]
}

try:
    response = requests.post(url, headers=headers, params=params, json=data)
    response.raise_for_status()

    # Extract base64 audio data from response
    audio_base64 = response.json()['data']['base64']

    # Decode base64 audio data
    audio_data = base64.b64decode(audio_base64)

    # Load audio data
    audio = AudioSegment.from_file(io.BytesIO(audio_data))

    subprocess.run(["bash", "notification.sh", "{}".format(sys.argv[1])])

    # Play audio
    play(audio)

except Exception as e:
    print(f"Error: {e}")
