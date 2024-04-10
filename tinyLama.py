import os
import torch
from transformers import pipeline

# Set the environment variable HSA_OVERRIDE_GFX_VERSION=10.3.0
os.environ["HSA_OVERRIDE_GFX_VERSION"] = "10.3.0"

# Check if CUDA (GPU support) is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Load the text generation pipeline with PyTorch backend
pipe = pipeline("text-generation",
                model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                framework="pt",
                device=device,
                # max_length=200,  # Adjust the maximum length of the response
                num_return_sequences=1)  # Adjust the number of returned sequences


def chat_bot(prompt):
    # We use the tokenizer's chat template to format each message
    messages = [
        {
            "role": "system",
            "content": "You will talk as the first person",
        },
        {"role": "user", "content": prompt},
    ]
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt)
    return outputs
    # return outputs[0]["generated_text"]


# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    response = chat_bot(user_input)
    print("Bot:", response)
