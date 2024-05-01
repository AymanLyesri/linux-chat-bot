response = """```command
ls -l
```

```command
ls -l
```"""


# Split the response string by "```command" to extract individual command blocks
command_blocks = response.split("```command")
commands = []

# Iterate over each command block (excluding the first block, which contains text before the first command)
for block in command_blocks[1:]:
    # Remove leading and trailing whitespace from the block
    block = block.strip()

    # Extract the command from the block (up to the first newline character)
    command = block.split("\n", 1)[0].strip()

    # Add the command to the list of commands
    commands.append(command)

# Join the commands with '&&' to create a single command string
command_string = ' && '.join(commands)

# Process the command (e.g., execute it)
print("Processing command:", command_string)
