import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import random
import string

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("500x400")

        # Initialize password data
        self.passwords = {
            "Facebook": "P@ssw0rd",
            "Twitter": "password123",
            "Instagram": "SecurePassword123",
            "LinkedIn": "pass1234"
        }

        # Initialize password strength levels
        self.weak_strength = ['123456', 'password', '123456789', '12345678', '12345', '1234567', '1234567890',
                              '123123', '111111', 'abc123', 'qwerty', 'password1']
        self.medium_strength = ['1234567', '1234567890', '123123', '111111', 'abc123', 'qwerty', 'password1',
                                'iloveyou', '123456a', 'admin', 'welcome']
        self.strong_strength = ['P@ssw0rd!', 'SecurePassword123', 'StrongPassword!123', 'P@55w0rd!',
                                'SuperSecurePassword!']

        # Create UI elements
        self.label_title = tk.Label(self.root, text="Decrypted Passwords", font=("Helvetica", 18))
        self.label_title.pack(pady=10)

        self.scroll_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.scroll_text.pack(pady=10)

        self.display_passwords()

    def display_passwords(self):
        self.scroll_text.delete(1.0, tk.END)
        for platform, password in self.passwords.items():
            strength = self.check_password_strength(password)
            self.scroll_text.insert(tk.END, f"{platform}: {password} - {strength}\n\n")

    def check_password_strength(self, password):
        if len(password) < 8:
            return "Weak"
        elif password.lower() in self.weak_strength:
            return "Weak"
        elif password.lower() in self.medium_strength:
            return "Medium"
        elif password.lower() in self.strong_strength:
            return "Strong"
        else:
            return "Strong"

# Initialize Tkinter app
root = tk.Tk()
app = PasswordManagerApp(root)
root.mainloop()
