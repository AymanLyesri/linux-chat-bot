import requests
import os

# URL of the model files (replace with the actual URL)
model_url = "https://huggingface.co/gpt2/resolve/main/pytorch_model.bin"

# Directory to save the model files
model_directory = "gpt2_model"

# Create the directory if it doesn't exist
if not os.path.exists(model_directory):
    os.makedirs(model_directory)

# Download the model file
response = requests.get(model_url)
if response.status_code == 200:
    with open(os.path.join(model_directory, "pytorch_model.bin"), "wb") as f:
        f.write(response.content)
    print("Model downloaded successfully.")
else:
    print("Failed to download model. Status code:", response.status_code)
