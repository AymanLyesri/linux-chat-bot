import json
import random
import csv
from itertools import product

# Step 1: Read the JSON file
with open('DATA/workspaceData/data.json', 'r') as json_file:
    data = json.load(json_file)

# Step 2: Parse the JSON data
instructions = data["instructions"]
responses = data["responses"]

# Define workspace numbers and expanded variations for user commands and assistant responses
workspace_numbers = list(range(1, 11))

# Ensure more combinations than required to guarantee uniqueness
all_possible_combinations = list(product(
    workspace_numbers, instructions, responses))

# Shuffle to ensure a random selection of combinations
random.shuffle(all_possible_combinations)

# Select the first 1000 unique combinations
selected_combinations = all_possible_combinations[:1000]

# Generate CSV content
csv_content = [["input", "response", "command", "text"]]
for number, instructions, response in selected_combinations:
    input_text = instructions.format(number)

    response = response.format(number, number)

    command = f"hyprctl dispatch {number}"

    chat_text = f"### Human: {input_text}\n### Assistant: {response}\n### Command: {command}"

    csv_content.append([input_text, response, command, chat_text])

# Write to CSV file
with open("train.csv", "a", newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_content)

print(
    f"CSV file has been add on with {len(selected_combinations)} samples.")
