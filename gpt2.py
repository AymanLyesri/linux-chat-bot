from transformers import pipeline, set_seed

# Check if GPU is available
# -1 for CPU, 0 for GPU
device = -1 if not pipeline("text-generation", device=0) else 0

generator = pipeline('text-generation', model='gpt2', device=device)
set_seed(42)

prompt = "Hello, I'm a language model,"
max_length = 30
num_return_sequences = 5

generated_sequences = generator(prompt,
                                max_length=max_length,
                                num_return_sequences=num_return_sequences)

for i, sequence in enumerate(generated_sequences):
    print(f"Generated Sequence {i + 1}: {sequence['generated_text']}")

if device == 0:
    print("Using GPU.")
else:
    print("Using CPU.")
