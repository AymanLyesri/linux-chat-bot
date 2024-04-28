import re


sentence = " honutoeu```\\nhyprctl dispatch workspace 1\\n``` More text here"
command = re.search(r'```(.*?)```', sentence).group(1)
remaining_sentence = re.sub(r'```(.*?)```', '', sentence)

print("Command: ", command)
print("Remaining Sentence: ", remaining_sentence)
