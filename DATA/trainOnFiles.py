import csv
import random
from itertools import product

# Define bash commands and their corresponding responses
bash_commands = {
    "create_file": "touch",
    "create_folder": "mkdir",
    "delete_file": "rm",
    "delete_folder": "rmdir",
    "display_file": "cat",
}

# Define file and folder names
files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]
folders = ["folder1", "folder2", "folder3", "folder4", "folder5"]

# Define corresponding instructions for each operation
inputs = {
    "create_file": [
        "Create a file named",
        "Add a new file called",
        "Generate a file named",
        "Make a new file called",
        "Craft a file named",
        "Put together a file named"
    ],
    "create_folder": [
        "Create a folder named",
        "Add a new folder called",
        "Generate a folder named",
        "Make a new folder called",
        "Craft a folder named",
        "Put together a folder named"
    ],
    "delete_file": [
        "Delete the file named",
        "Remove the file called",
        "Erase the file named",
        "Get rid of the file named",
        "Eliminate the file named",
        "Wipe out the file named"
    ],
    "delete_folder": [
        "Delete the folder named",
        "Remove the folder called",
        "Erase the folder named",
        "Get rid of the folder named",
        "Eliminate the folder named",
        "Wipe out the folder named"
    ],
    "display_file": [
        "Display the file named",
        "Show the content of the file called",
        "View the file named",
        "Read the content of the file called",
        "Present the file named",
        "Open and show the content of the file named"
    ],
}

responses = {
    "create": [
        "It's created, eager for your touch.",
        "A fresh file emerges, awaiting your command.",
        "A new file awaits, ready for your desires.",
        "Crafted, yearning for your direction.",
        "Forged, anticipating your guidance.",
        "Spawned, awaiting your influence."
    ],
    "delete": [
        "Deleted, leaving echoes behind.",
        "Gone, but the void craves your next move.",
        "Erased, yet its memory lingers.",
        "Vanished, leaving whispers in its wake.",
        "Evaporated, the void hungers for your choice.",
        "Eliminated, yet its essence persists."
    ],
    "display": [
        "Unveiled, secrets laid bare.",
        "Revealed, awaiting your exploration.",
        "Displayed, ready for your scrutiny.",
        "Exposed, secrets laid out for your perusal.",
        "Uncovered, inviting your inspection.",
        "Presented, poised for your examination."
    ]
}

# Get all possible combinations
all_combinations = []
for command, operation in bash_commands.items():
    if "file" in command:
        targets = files
    else:
        targets = folders
    for target in targets:
        for input_instruction in inputs[command]:
            all_combinations.append((operation, target, input_instruction))

# Shuffle combinations for randomness
random.shuffle(all_combinations)

# Generate CSV content
csv_content = [["input", "output", "text"]]
response = ""
for operation, target, input_instruction in all_combinations:
    if "create" in command:
        response = random.choice(responses["create"])
    elif "delete" in command:
        response = random.choice(responses["delete"])
    elif "display" in command:
        response = random.choice(responses["display"])

    output_text = f"{response} | {operation} {target}"
    input_text = f"{input_instruction} {target}"
    text = f"### Human: {input_text} ### Assistant: {output_text}"

    csv_content.append([input_text, output_text, text])

# Write to CSV file
csv_filename = "train.csv"
with open(csv_filename, "w", newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_content)

print(
    f"CSV file '{csv_filename}' has been generated with {len(all_combinations)} samples.")
