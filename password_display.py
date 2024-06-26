import tkinter as tk
from tkinter import scrolledtext
import string
import mysql.connector
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

class ViewPasswords:
    def __init__(self, root, logged_in_user_id):  # Accept logged_in_user_id as a parameter
        self.root = root
        self.root.title("View Passwords")
        self.root.geometry("500x400")
        self.logged_in_user_id = logged_in_user_id  # Store logged_in_user_id as an attribute

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2302",
            database="siguria"
        )

        # Create UI elements
        self.label_title = tk.Label(self.root, text="Decrypted Passwords", font=("Arial", 20, "bold"), pady=10)
        self.label_title.pack()

        self.scroll_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=15, font=("Arial", 12))
        self.scroll_text.pack(pady=10)

        # Apply styling
        self.scroll_text.tag_configure("weak", foreground="red")
        self.scroll_text.tag_configure("medium", foreground="orange")
        self.scroll_text.tag_configure("strong", foreground="green")

        # Display passwords with styling
        self.display_passwords()

    def decrypt_password(self, encrypted_password):
        # Initialize AES cipher
        key = b'Sixteen byte key'
        cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])

        # Decode and decrypt password
        encrypted_password_bytes = base64.b64decode(encrypted_password.encode())
        decrypted_password_bytes = unpad(cipher.decrypt(encrypted_password_bytes), AES.block_size)
        return decrypted_password_bytes.decode()

    def display_passwords(self):
        cursor = self.conn.cursor(dictionary=True)
        # Modify the query to include a WHERE clause for user_id
        query = "SELECT account, encrypted_pwd FROM tblpasswords WHERE user_id = %s"

        # Execute the query with the logged-in user ID as the parameter
        cursor.execute(query, (self.logged_in_user_id,))  # Use the stored logged_in_user_id
        for row in cursor.fetchall():
            platform = row['account']
            encrypted_password = row['encrypted_pwd']
            decrypted_password = self.decrypt_password(encrypted_password)
            strength = self.check_password_strength(decrypted_password)
            self.scroll_text.insert(tk.END, f"{platform}: {decrypted_password} - ", strength)
            self.scroll_text.insert(tk.END, f"{strength}\n\n", strength)

    def check_password_strength(self, password):
        weak_strength = ['123456', 'password', '123456789', '12345678', '12345', '1234567', '1234567890',
                        '123123', '111111', 'abc123', 'qwerty', 'password1']
        medium_strength = ['1234567', '1234567890', '123123', '111111', 'abc123', 'qwerty', 'password1',
                        'iloveyou', '123456a', 'admin', 'welcome']
        strong_strength = ['P@ssw0rd!', 'SecurePassword123', 'StrongPassword!123', 'P@55w0rd!',
                        'SuperSecurePassword!']

        # Check password strength
        if password.lower() in weak_strength or len(password) < 8:
            return "weak"
        elif password.lower() in medium_strength:
            return "medium"
        elif password.lower() in strong_strength or all(c in string.ascii_letters + string.digits + string.punctuation for c in password) and len(password) >= 12:
            return "strong"
        else:
            return "strong"  # Default to strong if unknown

