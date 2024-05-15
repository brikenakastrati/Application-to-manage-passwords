import tkinter as tk
from tkinter import ttk
from add_password import AddPassword
from update_password import UpdatePassword
from password_display import ViewPasswords

class LandingPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("400x200")
        self.configure(background="#f0f0f0")

        # Style for buttons
        style = ttk.Style()
        style.configure('TButton', background='#007bff', foreground='white')

        # Create and place buttons
        add_button = ttk.Button(self, text="Add Password", command=self.open_add_password)
        add_button.pack(pady=10)

        update_button = ttk.Button(self, text="Update Password", command=self.open_update_password)
        update_button.pack(pady=10)

        view_button = ttk.Button(self, text="View Passwords", command=self.open_view_passwords)
        view_button.pack(pady=10)

    def open_add_password(self):
        add_password_window = AddPassword()
        add_password_window.mainloop()

    def open_update_password(self):
        update_password_window = UpdatePassword()
        update_password_window.mainloop()

    def open_view_passwords(self):
        view_passwords_window = ViewPasswords()
        view_passwords_window.mainloop()

if __name__ == "__main__":
    app = LandingPage()
    app.mainloop()
