sentence = "honutoeu ```bash\nhyprctl dispatch workspace 1\n```"
start, command, end = sentence.split("```")
command = command.replace("bash\n", "").strip()

print("Command:", command)
print("Clean Text:", start.strip()+" " + end.strip())
