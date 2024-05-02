import re
sentence = """```command
echo "
## Getting Started

To get started with our project, follow these simple steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the necessary dependencies using the command: 
   \`\`\`
   pip install -r requirements.txt
   \`\`\`
4. Run the main script by executing:
   \`\`\`
   python main.py
   \`\`\`

That's it! You're all set to start coding with Angel Ai. Happy coding! 🌟
" >> README.md
```"""

sentence = sentence.replace("\\`", "")

# Use regular expressions to find all occurrences of "```command <command>```" in the sentence
commands = re.findall(r"```command\n([^`]+)```", sentence)

# Store the commands in an array
commands_array = [command.strip() for command in commands]

# Replace all occurrences of "```command <command>```" with an empty string
remaining_sentence = re.sub(r"```command\n([^`]+)```", "", sentence)

# Strip any leading or trailing whitespace from the remaining sentence
remaining_sentence = remaining_sentence.replace("\n", " ").strip()

print("Commands array:", commands_array)
print("Remaining sentence:", remaining_sentence)
