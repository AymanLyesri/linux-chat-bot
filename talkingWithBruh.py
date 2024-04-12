import os
import subprocess
from typing import List
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Set the environment variable HSA_OVERRIDE_GFX_VERSION=10.3.0
os.environ["HSA_OVERRIDE_GFX_VERSION"] = "10.3.0"

# Check if CUDA (GPU support) is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model_name = "bruh1"  # You can replace "gpt2" with any other compatible model name

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Move model to the appropriate device
model.to(device)


def formatted_prompt(question) -> str:
    return f"""### Human:
{question}
### Assistant:"""


def generate_response(input) -> List[str]:

    formatted_input = formatted_prompt(input)

    input_tokens = tokenizer.encode(formatted_input, return_tensors="pt")

    # Move input_tokens to the appropriate device
    input_tokens = input_tokens.to(device)

    # Generate a sequence of tokens following the input
    output_tokens = model.generate(
        input_tokens, temperature=0.7, do_sample=True)

    # Decode the generated tokens to a string
    generated_text = tokenizer.decode(
        output_tokens[0], skip_special_tokens=True)

    # Check if generated_text can be split
    if "|" in generated_text:
        response, command = generated_text.split("|", 1)
        # Extract the text after "### Assistant:"
        response = response[response.find("### Assistant:") +
                            len("### Assistant:"):].strip()
        return [response, command]
    else:
        # Return generated_text without splitting
        response = generated_text[generated_text.find("### Assistant:") +
                                  len("### Assistant:"):].strip()
        return [generated_text.strip(), ""]


# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    response = generate_response(user_input)

    print("Bot:", response[0])
    subprocess.run(["python", "speech2.py", "{}".format(response[0])])

    print("Command:", response[1])
