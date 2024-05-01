import requests
from playsound import playsound

url = "https://tts-universal.p.rapidapi.com/tts/v1/"

payload = {
    "text": "Hello, what is your name ?",
    "tts_service": "azure",
    "voice_indentifier": "en-US-AmberNeural"
}
headers = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Key": "eda5c736e8msha192a972ef3bc0bp175619jsn8694b5f19f74",
    "X-RapidAPI-Host": "tts-universal.p.rapidapi.com"
}

try:
    # Post request to convert text to speech
    response = requests.post(url, data=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response JSON
        print(response.json())

        # Get the URL of the audio file from the response JSON
        audio_url = response.json()["result"]

        # Send a GET request to download the audio file
        audio_response = requests.get(audio_url)

        # Check if the request was successful
        if audio_response.status_code == 200:
            # Save the audio content to a temporary file
            with open('temp_audio.mp3', 'wb') as f:
                f.write(audio_response.content)

            # Play the audio file
            playsound('temp_audio.mp3')
        else:
            print(
                f"Failed to download audio file. Status code: {audio_response.status_code}")
    else:
        print(
            f"Failed to convert text to speech. Status code: {response.status_code}")

except requests.RequestException as e:
    print(f"An error occurred: {e}")
