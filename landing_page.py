import tkinter as tk
from tkinter import ttk
from add_password import AddPassword
from update_password import UpdatePassword
from password_display import ViewPasswords

class LandingPage(tk.Tk):
    def __init__(self, logged_in_user_id):
        super().__init__()
        self.title("Password Manager")
        self.geometry("400x300")
        self.configure(background="#f0f0f0")
        self.logged_in_user_id = logged_in_user_id  # Store logged_in_user_id as an attribute
  # Create a title label
        title_label = ttk.Label(self, text="Welcome to Password Manager", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=20)
        
        # Style for buttons
        style = ttk.Style()
        style.configure('TButton', background='#007bff', foreground='black', font=('Helvetica', 10), padding=10)

        # Create and place buttons
        add_button = ttk.Button(self, text="➕Add Password", command=self.open_add_password)
        add_button.pack(pady=10)

        update_button = ttk.Button(self, text="✏️Update Password", command=self.open_update_password)
        update_button.pack(pady=10)

        view_button = ttk.Button(self, text="🔍View Passwords", command=self.open_view_passwords)
        view_button.pack(pady=10)

    def open_add_password(self):
        add_password_window = tk.Toplevel(self)
        AddPassword(add_password_window,self.logged_in_user_id)

    def open_update_password(self):
        update_password_window = tk.Toplevel(self)
        UpdatePassword(update_password_window,self.logged_in_user_id)

    def open_view_passwords(self):
        view_passwords_window = tk.Toplevel(self)
        ViewPasswords(view_passwords_window,self.logged_in_user_id)

    @staticmethod
    def start_application(logged_in_user_id):
        app = LandingPage(logged_in_user_id)  # Pass logged_in_user_id to LandingPage
        app.mainloop()
