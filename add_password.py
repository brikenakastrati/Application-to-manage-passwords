import tkinter as tk
from tkinter import messagebox
import mysql.connector
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import string 
import random

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
            password="2302",
            database="siguria"
        )
         # Create a title label
        title_label = ttk.Label(master, text="Add New Password", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=20)
        
        # Labels and Entries
        tk.Label(root, text="Account:").grid(row=0, column=0, padx=10, pady=10)
        self.account_entry = tk.Entry(root)
        self.account_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(root, show="*")

        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
         tk.Label(root, text="(8-20 characters)", font=("Helvetica", 8), fg="gray").pack()

        # Button to save password
        tk.Button(root, text="Save", command=self.save_password).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Suggest Strong Password", command=self.suggest_password).grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Toggle Password Visibility", command=self.toggle_password_visibility).grid(row=4, column=0, columnspan=2, pady=5)

    def encrypt_password(self, password):
        key = b'Sixteen byte key'  # 16-byte key for AES
        cipher = AES.new(key, AES.MODE_CBC, iv=key[:16])  # Initialize AES cipher
        padded_password = pad(password.encode(), AES.block_size)  # Pad the password to make it multiple of block size
        encrypted_password = base64.b64encode(cipher.encrypt(padded_password))  # Encrypt and encode the password
        return encrypted_password.decode()
    

    def generate_strong_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        strong_password = ''.join(random.choice(characters) for i in range(16)) 
        return strong_password

    def suggest_password(self):
        suggested_password = self.generate_strong_password()
        self.password_entry.delete(0, tk.END)  
        self.password_entry.insert(0, suggested_password) 
        self.password_entry.config(show='')  

    def toggle_password_visibility(self):
     if self.password_entry.cget('show') == '*':
        self.password_entry.config(show='')  
     else:
        self.password_entry.config(show='*') 




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

