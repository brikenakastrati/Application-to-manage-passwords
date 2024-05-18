from tkinter import *
from tkinter import messagebox
import mysql.connector
import random
import string
from cryptography.fernet import Fernet
import hashlib
import subprocess
from landing_page import LandingPage

def connect():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2302",
            database="siguria"
        )
        if conn.is_connected():
            print("Lidhja me MySQL është bërë me sukses")
            return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Gabim në Lidhje", f"Gabim në lidhjen me bazën e të dhënave: {e}")


def generate_aes_key():
    return Fernet.generate_key()


def create_aes_cipher(key):
    return Fernet(key)

def encrypt_password(aes_cipher, password):
    return aes_cipher.encrypt(password.encode())

def decrypt_password(aes_cipher, encrypted_password):
    return aes_cipher.decrypt(encrypted_password).decode()


def save_encrypted_password(conn, full_name, email, encrypted_password):
    try:
        cursor = conn.cursor()
        query_insert_user = "INSERT INTO tblusers (full_name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query_insert_user, (full_name, email, encrypted_password))
        conn.commit()
        messagebox.showinfo("Sukses në Regjistrim", "Regjistrimi u krye me sukses.")
    except mysql.connector.Error as e:
        messagebox.showerror("Gabim në Regjistrim", f"Gabim në regjistrim: {e}")
        conn.rollback()


def get_encrypted_password(conn, email):
    try:
        cursor = conn.cursor()
        query_get_password = "SELECT password FROM tblusers WHERE email = %s"
        cursor.execute(query_get_password, (email,))
        encrypted_password = cursor.fetchone()
        return encrypted_password[0] if encrypted_password else None
    except mysql.connector.Error as e:
        messagebox.showerror("Gabim në Marrje të Fjalëkalimit", f"Gabim në marrjen e fjalëkalimit: {e}")
        return None

def signup(conn, full_name, email, password):
    try:
        cursor = conn.cursor()
        if not email or not password or not full_name:
            messagebox.showerror("Gabim në Regjistrim", "Emaili dhe fjalëkalimi duhet të plotësohen.")
            return 
        
      
        query_check_email = "SELECT * FROM tblusers WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Gabim në Regjistrim", "Ekziston një përdorues me këtë email.")
            return
        
      
        aes_key = generate_aes_key()
        aes_cipher = create_aes_cipher(aes_key)
       

        encrypted_password = encrypt_password(aes_cipher, password)
        
      
        query_insert_user = "INSERT INTO tblusers (full_name, email, password, aes_key) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_insert_user, (full_name, email, encrypted_password, aes_key))
        conn.commit()
        
        messagebox.showinfo("Sukses në Regjistrim", "Regjistrimi u krye me sukses.")
    except mysql.connector.Error as e:
        messagebox.showerror("Gabim në Regjistrim", f"Gabim në regjistrim: {e}")
        conn.rollback()


def switch_to_login():
    global login_email_entry, login_password_entry  # Define global variables here
    root.destroy() 
    login_window = Tk()  
    login_window.title("Hyrja në Sistem")

  
    Label(login_window, text="Email:").pack()
    login_email_entry = Entry(login_window)
    login_email_entry.pack()
    Label(login_window, text="Password:").pack()
    login_password_entry = Entry(login_window, show="*")
    login_password_entry.pack()
    Button(login_window, text="Log in", command=on_login).pack()

    login_window.mainloop()  


def on_login():
    global login_email_entry, login_password_entry, logged_in_user_id  # Declare logged_in_user_id as global
    
   
    email = login_email_entry.get()
    password = login_password_entry.get()
    
 
    if not email or not password:
        messagebox.showerror("Gabim në Hyrje", "Ju lutem vendosni email-in dhe fjalëkalimin.")
        return
    
  
    conn = connect()

    if conn:
        try:
            cursor = conn.cursor()
            
         
            encrypted_password_db = get_encrypted_password(conn, email)
            if encrypted_password_db:
            
                aes_key = get_aes_key_from_db(conn, email)
                if aes_key:
                  
                    aes_cipher = create_aes_cipher(aes_key)
                    
                 
                    decrypted_password_db = decrypt_password(aes_cipher, encrypted_password_db)
                    
                  
                    if decrypted_password_db == password:  
                        try:
                            global logged_in_user_id  # Declare logged_in_user_id as global
                            logged_in_user_id = get_user_id_from_db(conn, email)  # Update the global variable
                            LandingPage.start_application(logged_in_user_id)
                        except FileNotFoundError:
                            print("Gabim: Skripta nuk u gjet.")
                        
                        
                    else:
                        messagebox.showerror("Gabim në Hyrje", "Email-i ose fjalëkalimi është i pasaktë.")
                else:
                    messagebox.showerror("Gabim në Hyrje", "Çelësi AES nuk u gjet për këtë përdorues.")
            else:
                messagebox.showerror("Gabim në Hyrje", "Email-i ose fjalëkalimi është i pasaktë.")
                return
            
        except mysql.connector.Error as e:
            messagebox.showerror("Gabim në Hyrje", f"Gabim në verifikimin e përdoruesit: {e}")
            
        finally:
            cursor.close()  
            conn.close()  
    else:
        messagebox.showerror("Gabim në Hyrje", "Lidhja me bazën e të dhënave dështoi.")

def get_logged_in_user_id():
    return logged_in_user_id
def get_user_id_from_db(conn, email):
    try:
        cursor = conn.cursor()
        query_get_user_id = "SELECT user_id FROM tblusers WHERE email = %s"
        cursor.execute(query_get_user_id, (email,))
        user_id = cursor.fetchone()
        return user_id[0] if user_id else None
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error retrieving user ID: {e}")
        return None
    


def get_aes_key_from_db(conn, email):
    try:
        cursor = conn.cursor()
        query_get_aes_key = "SELECT aes_key FROM tblusers WHERE email = %s"
        cursor.execute(query_get_aes_key, (email,))
        aes_key = cursor.fetchone()
        return aes_key[0] if aes_key else None
    except mysql.connector.Error as e:
        messagebox.showerror("Gabim në Marrje të Çelësit AES", f"Gabim në marrjen e çelësit AES: {e}")
        return None


def generate_strong_password():
    length = 12  
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def suggest_strong_password():
    suggested_password = generate_strong_password()
    confirmation = messagebox.askyesno("🔒 Sugjerimi i Fjalëkalimit", f"Sugjerimi: {suggested_password}\n\nA dëshironi ta përdorni këtë sugjerim?")
    if confirmation:
        password_entry.delete(0, END)
        password_entry.insert(0, suggested_password)
        
    return suggested_password if confirmation else None


def on_use_suggested_password(suggested_password):
    password_entry.delete(0, END)
    password_entry.insert(0, suggested_password)
    messagebox.showinfo("🔒 Sugjerimi i Fjalëkalimit", "Fjalëkalimi i sugjeruar është vendosur.")


def on_signup():
    full_name = full_name_entry.get()
    email = email_entry.get()
    password = password_entry.get()

  
    if not password:
      
        suggested_password = suggest_strong_password()
        return

    conn = connect()
    if conn:
        signup(conn, full_name, email, password)
        switch_to_login() 


root = Tk()
root.title("Register")

# Labels dhe Entries
Label(root, text="Name:").pack()
full_name_entry = Entry(root)
full_name_entry.pack()
Label(root, text="Email:").pack()
email_entry = Entry(root)
email_entry.pack()
Label(root, text="Password:").pack()
password_entry = Entry(root, show="*")
password_entry.pack()


suggest_password_button = Button(root, text="Suggest a strong password", command=suggest_strong_password, fg="blue")
suggest_password_button.pack()


Button(root, text="Register", command=on_signup).pack()

login_button = Button(root, text="Go to log in", command=switch_to_login, fg="blue")
login_button.pack(side=BOTTOM)

root.mainloop()
