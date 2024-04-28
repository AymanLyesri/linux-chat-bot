import re


def remove_multiple_enclosed_words(text):
    # Define a regular expression pattern to match multiple words enclosed in asterisks
    pattern = r'\*(\w+(?:\s+\w+)*)(?=[.,?!]?)(?=\s*[.,?!])\*'

    # Use sub() function to replace matched patterns with an empty string
    result = re.sub(pattern, '', text)

    return result.strip()


# Example usage
text = "*giggles and laughs* Your wish is my command! I'm always happy when I'm chatting with you, *cutie*."
result = remove_multiple_enclosed_words(text)
print(result)
