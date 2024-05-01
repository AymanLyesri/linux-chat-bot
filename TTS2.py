import io
import requests
import time
from pydub import AudioSegment
from pydub.playback import play

url = "https://large-text-to-speech.p.rapidapi.com/tts"

payload = {
    "text": sys.arg
}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "eda5c736e8msha192a972ef3bc0bp175619jsn8694b5f19f74",
    "X-RapidAPI-Host": "large-text-to-speech.p.rapidapi.com"
}

# Post request to convert text to speech
response = requests.post(url, json=payload, headers=headers)

# Print the response containing the job ID
print(response.json())

# Extract the job ID from the response
job_id = response.json()["id"]

# Prepare the query string with the job ID
querystring = {"id": job_id}

# Initialize a flag to indicate if conversion is complete
conversion_complete = False

# Loop until conversion is complete
while not conversion_complete:
    # Get request to check the status of the conversion job
    response = requests.get(url, headers=headers, params=querystring)

    # Extract the status from the response
    status = response.json()["status"]

    # Print the status
    print(f"Conversion status: {status}")

    # Check if conversion is complete
    if status == "success":
        conversion_complete = True
    else:
        # Wait for a few seconds before checking again
        time.sleep(1)

# Download the audio file
response = requests.get(response.json()["url"])

# Load the audio file
audio = AudioSegment.from_file(io.BytesIO(response.content))

# Play the audio file
play(audio)
