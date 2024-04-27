import csv
import json
import random
from itertools import product

# Step 1: Read the JSON file
with open('DATA/fileManipulation/data.json', 'r') as json_file:
    data = json.load(json_file)

# Step 2: Parse the JSON data
bash_commands = data["bash_commands"]
files = data["files"]
folders = data["folders"]
inputs = data["inputs"]
responses = data["responses"]

# Get all possible combinations
all_combinations = []
for operation, command in bash_commands.items():
    if "file" in operation:
        targets = files
    else:
        targets = folders
    for target in targets:
        for instruction in inputs[operation]:
            all_combinations.append((instruction, target, operation, command))

# Shuffle combinations for randomness
random.shuffle(all_combinations)

# Generate CSV content
csv_content = [["input", "response", "command", "text"]]

# Limit to 500 combinations
for instruction, target, operation, command in all_combinations[:500]:
    response = random.choice(responses[operation])
    command = f"{command} {target}"
    input = f"{instruction} {target}"
    text = f"### Human: {input}\n### Assistant: {response}\n### Command: {command}"

    csv_content.append([input, response, command, text])

# Write to CSV file
csv_filename = "train.csv"
with open(csv_filename, "a", newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_content)

print(
    f"CSV file '{csv_filename}' has been generated with {len(all_combinations[:500])} samples.")
