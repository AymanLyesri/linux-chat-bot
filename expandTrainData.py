import random
import csv
from itertools import product, permutations

# Expand variations for user commands and assistant responses
workspace_numbers = list(range(1, 11))
user_commands_expanded = [
    "workspace {} now",
    "pls switch to ws {}",
    "activate wsp {}",
    "I need workspace {}",
    "move me to workspace {}",
    "can we go to workspace {}?",
    "how about workspace {}?",
    "workspace {} stat",
    "quickly, workspace {}",
    "set workspace to {}",
    "let's go to workspace {}",
    "wsp {} please",
    "to {}th workspace",
    "workspace {}, please",
    "need to switch to workspace {}"
]
assistant_responses_expanded = [
    "Now switching to workspace {} | hyprctl dispatch {}",
    "Alright, moving to workspace {} | hyprctl dispatch {}",
    "Workspace {} is now active | hyprctl dispatch {}",
    "Let's head over to workspace {} | hyprctl dispatch {}",
    "Okay, going to workspace {} | hyprctl dispatch {}",
    "Consider it done. Workspace {} | hyprctl dispatch {}",
    "Sure, workspace {} coming up | hyprctl dispatch {}",
    "Done. You're in workspace {} now | hyprctl dispatch {}",
    "Workspace {} is ready for you | hyprctl dispatch {}",
    "Transitioning to workspace {} | hyprctl dispatch {}"
]

# Ensure more combinations than required to guarantee uniqueness
all_possible_combinations = list(product(
    workspace_numbers, user_commands_expanded, assistant_responses_expanded))

# Shuffle to ensure a random selection of combinations
random.shuffle(all_possible_combinations)

# Select the first 200 unique combinations
selected_combinations = all_possible_combinations[:200]

# Generate CSV content
csv_content = [["INPUT", "OUTPUT", "text"]]
for number, user_cmd, assistant_rsp in selected_combinations:
    input_text = user_cmd.format(number)
    output_text = assistant_rsp.format(number, number)
    chat_text = f'<user>{input_text}</user><assistant>{output_text}</assistant>'
    csv_content.append([input_text, output_text, chat_text])

# Write to CSV file
csv_filename = "expanded_workspace_commands.csv"
with open(csv_filename, "w", newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_content)

print(
    f"CSV file '{csv_filename}' has been generated with {len(selected_combinations)} samples.")
