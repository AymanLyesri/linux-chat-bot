import tkinter as tk
from tkinter import Scrollbar
import json
import process


class ChatInterface:
    def __init__(self, master):
        self.master = master
        master.title("ChatGPT")

        # Dark mode color scheme
        self.bg_color = "#212121"
        self.text_color = "#FFFFFF"

        # Create and pack the conversation history display
        self.conversation_display = tk.Text(
            master, state='disabled', bg=self.bg_color, fg=self.text_color)
        self.conversation_display.pack(fill=tk.BOTH, expand=True)

        # Create a scrollbar for the conversation display
        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link scrollbar to conversation display
        self.scrollbar.config(command=self.conversation_display.yview)
        self.conversation_display.config(yscrollcommand=self.scrollbar.set)

        # Create and pack the user input field
        self.user_input = tk.Entry(
            master, bg=self.bg_color, fg=self.text_color)
        self.user_input.pack(fill=tk.X)

        # Bind the user input field to the Enter key
        self.user_input.bind("<Return>", process.process_input_gui(self))

        # Load conversation history from file
        self.load_history("conversation_history.json")

    def load_history(self, filename):
        try:
            with open("dialogue_history.json", "r") as file:
                history = json.load(file)
                for item in history:
                    role = item.get("role", "")
                    content = item.get("content", "")
                    if role and content:
                        if role == "user":
                            self.display_message(
                                "================================================\n")
                        message = role.capitalize() + ": " + content
                        self.display_message(message)
        except FileNotFoundError:
            # If history file not found, ignore and continue
            pass

    def display_message(self, message):
        self.conversation_display.config(state='normal')
        self.conversation_display.insert(
            tk.END, message + "\n")
        self.conversation_display.config(state='disabled')
        self.conversation_display.see("end")


# Create and run the Tkinter application
root = tk.Tk()
app = ChatInterface(root)

# Configure dark mode colors
root.config(bg="#212121")
root.mainloop()
