import requests
from playsound import playsound
import config

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/ckLJFnjxNzXtnh5nryPK"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "74096c2b70974d25b5b97f5dbfbcffe6"
}


def speech2(speech):
    data = {
        "text": speech,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)
    with open(config.PATH+'speech.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    playsound(config.PATH+'speech.mp3')
