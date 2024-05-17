import tkinter as tk
from tkinter import messagebox
import mysql.connector
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from login_signup import get_logged_in_user_id

class UpdatePassword:
    def __init__(self, root):
        self.root = root
        self.root.title("Update Password")
        self.root.geometry("400x200")
        
        # Connect to the database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2302",
            database="siguria"
        )

        # Labels and Entries
        tk.Label(root, text="Account:").pack(padx=10, pady=10)
        self.account_entry = tk.Entry(root)
        self.account_entry.pack(padx=10, pady=10)

        tk.Label(root, text="New Password:").pack(padx=10, pady=10)
        self.new_password_entry = tk.Entry(root, show="*")
        self.new_password_entry.pack(padx=10, pady=10)

        # Button to update password
        tk.Button(root, text="Update", command=self.update_password).pack(padx=10, pady=10)

    def encrypt_password(self, password):
        key = b'Sixteen byte key'  # 16-byte key for AES
        cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])  # Initialize AES cipher
        padded_password = pad(password.encode(), AES.block_size)  # Pad the password to make it multiple of block size
        encrypted_password = base64.b64encode(cipher.encrypt(padded_password))  # Encrypt and encode the password
        return encrypted_password.decode()

    def update_password(self):
        account = self.account_entry.get()
        new_password = self.new_password_entry.get()

        if not account or not new_password:
            messagebox.showerror("Error", "Please fill in both account and new password fields.")
            return

        encrypted_password = self.encrypt_password(new_password)

        cursor = self.conn.cursor()
        # Modify the query to include a WHERE clause for user_id and account
        query = "UPDATE tblpasswords SET encrypted_pwd = %s WHERE account = %s AND user_id = %s"

        # Assuming you have the values for encrypted_pwd and account
        logged_in_user_id = get_logged_in_user_id()
        values = (encrypted_password, account, logged_in_user_id)

        try:
            cursor.execute(query, values)
            self.conn.commit()
            messagebox.showinfo("Success", "Password updated successfully.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Failed to update password: {e}")
        finally:
            cursor.close()


