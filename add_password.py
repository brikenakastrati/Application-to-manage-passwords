import tkinter as tk
from tkinter import messagebox
import mysql.connector
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

class AddPassword:
    def __init__(self, root, logged_in_user_id):  # Accept logged_in_user_id as a parameter
        self.root = root
        self.root.title("Add Password")
        self.root.geometry("400x200")
        self.logged_in_user_id = logged_in_user_id  # Store logged_in_user_id as an attribute

        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="siguria"
        )

        # Labels and Entries
        tk.Label(root, text="Account:").grid(row=0, column=0, padx=10, pady=10)
        self.account_entry = tk.Entry(root)
        self.account_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Button to save password
        tk.Button(root, text="Save", command=self.save_password).grid(row=2, column=0, columnspan=2, pady=10)

    def encrypt_password(self, password):
        key = b'Sixteen byte key'  # 16-byte key for AES
        cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])  # Initialize AES cipher
        padded_password = pad(password.encode(), AES.block_size)  # Pad the password to make it multiple of block size
        encrypted_password = base64.b64encode(cipher.encrypt(padded_password))  # Encrypt and encode the password
        return encrypted_password.decode()

    def save_password(self):
        account = self.account_entry.get()
        password = self.password_entry.get()

        if not account or not password:
            messagebox.showerror("Error", "Please fill in both account and password fields.")
            return

        encrypted_password = self.encrypt_password(password)

        cursor = self.conn.cursor()
        query = "INSERT INTO tblpasswords (account, encrypted_pwd, user_id) VALUES (%s, %s, %s)"

        values = (account, encrypted_password, self.logged_in_user_id)  # Use the stored logged_in_user_id

        try:
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Password saved successfully.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Failed to save password: {e}")
        finally:
            cursor.close()

