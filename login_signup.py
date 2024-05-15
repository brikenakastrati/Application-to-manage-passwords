from tkinter import *
from tkinter import messagebox
import mysql.connector
import random
import string

# Lidhja me databazën
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

# Funksioni për regjistrimin e përdoruesve
def signup(conn, full_name, email, password):
    try:
        cursor = conn.cursor()
        
        # Kontrollo nëse ekziston një përdorues me të njëjtin email
        query_check_email = "SELECT * FROM tblusers WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Gabim në Regjistrim", "Ekziston një përdorues me këtë email.")
            return
        
        # Shto përdoruesin në bazën e të dhënave nëse nuk ekziston
        query_insert_user = "INSERT INTO tblusers (full_name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query_insert_user, (full_name, email, password))
        conn.commit()
        
        messagebox.showinfo("Sukses në Regjistrim", "Regjistrimi u krye me sukses.")
    except mysql.connector.Error as e:
        messagebox.showerror("Gabim në Regjistrim", f"Gabim në regjistrim: {e}")
        conn.rollback()

# Funksioni për ndryshimin e ndërfaqes pas regjistrimit
def switch_to_login():
    global login_email_entry, login_password_entry  # Define global variables here
    root.destroy()  # Mbylle dritaren e regjistrimit
    login_window = Tk()  # Krijo një dritare të re për hyrjen në sistem
    login_window.title("Hyrja në Sistem")

    # Krijimi i ndërfaqes për hyrjen në sistem (shto elementet e nevojshme këtu)
    Label(login_window, text="Email:").pack()
    login_email_entry = Entry(login_window)
    login_email_entry.pack()
    Label(login_window, text="Fjalëkalimi:").pack()
    login_password_entry = Entry(login_window, show="*")
    login_password_entry.pack()
    Button(login_window, text="Hyr", command=on_login).pack()

    login_window.mainloop()  # Fillimi i dritares së hyrjes në sistem

def on_login():
    global login_email_entry, login_password_entry
    
    # Merrni email-in dhe fjalëkalimin e vendosur
    email = login_email_entry.get()
    password = login_password_entry.get()
    
    # Kontrolloni nëse email-i dhe fjalëkalimi janë bosh
    if not email or not password:
        messagebox.showerror("Gabim në Hyrje", "Ju lutem vendosni email-in dhe fjalëkalimin.")
        return
    
    # Lidhuni me bazën e të dhënave
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Verifikoni kredencialet e përdoruesit
            query_check_credentials = "SELECT * FROM tblusers WHERE email = %s AND password = %s"
            cursor.execute(query_check_credentials, (email, password))
            user = cursor.fetchone()
            
            if user:
                messagebox.showinfo("Sukses në Hyrje", "Hyrja në sistem u krye me sukses.")
                # Bëni diçka pas hyrjes së suksesshme, si hapja e një dritare të re ose veprime të tjera
                
            else:
                messagebox.showerror("Gabim në Hyrje", "Email-i ose fjalëkalimi është i pasaktë.")
            
        except mysql.connector.Error as e:
            messagebox.showerror("Gabim në Hyrje", f"Gabim në verifikimin e përdoruesit: {e}")
            
        finally:
            cursor.close()  # Mbyll cursor-in
            conn.close()  # Mbyll lidhjen me bazën e të dhënave



# Funksioni për gjenerimin e një fjalëkalimi të fortë
def generate_strong_password():
    length = 12  # Gjatësia e sugjeruar e fjalëkalimit (mund të ndryshohet sipas nevojës)
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# Funksioni për sugjerimin e një fjalëkalimi të fortë
def suggest_strong_password():
    suggested_password = generate_strong_password()
    confirmation = messagebox.askyesno("Sugjerimi i Fjalëkalimit", f"Sugjerimi: {suggested_password}\n\nA dëshironi ta përdorni këtë sugjerim?")
    if confirmation:
        password_entry.delete(0, END)
        password_entry.insert(0, suggested_password)
        messagebox.showinfo("Sugjerimi i Fjalëkalimit", "Fjalëkalimi i sugjeruar është vendosur.")
    return suggested_password if confirmation else None

# Funksioni për përdorimin e sugjerimit të fjalëkalimit të fortë
def on_use_suggested_password(suggested_password):
    password_entry.delete(0, END)
    password_entry.insert(0, suggested_password)
    messagebox.showinfo("Sugjerimi i Fjalëkalimit", "Fjalëkalimi i sugjeruar është vendosur.")

# Funksioni i thirrur nga butoni 'Regjistrohu'
def on_signup():
    full_name = full_name_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Kontrollo nëse përdoruesi ka vendosur një fjalëkalim
    if not password:
        # Shfaq sugjerimin për një fjalëkalim të fortë
        suggested_password = suggest_strong_password()
        return

    conn = connect()
    if conn:
        signup(conn, full_name, email, password)
        switch_to_login()  # Ndryshimi i dritares pas regjistrimit

# Krijimi i ndërfaqes grafike për regjistrimin
root = Tk()
root.title("Regjistrimi")

# Labels dhe Entries
Label(root, text="Emri i Plotë:").pack()
full_name_entry = Entry(root)
full_name_entry.pack()
Label(root, text="Email:").pack()
email_entry = Entry(root)
email_entry.pack()
Label(root, text="Fjalëkalimi:").pack()
password_entry = Entry(root, show="*")
password_entry.pack()

# Button për sugjerimin e fjalëkalimit të fortë
suggest_password_button = Button(root, text="Sugjero Fjalëkalimin e Fortë", command=suggest_strong_password)
suggest_password_button.pack()

# Button për regjistrim
Button(root, text="Regjistrohu", command=on_signup).pack()

root.mainloop()
