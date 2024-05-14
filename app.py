import os
import base64
import json
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class PasswordManager:
    def __init__(self):
        self.backend = default_backend()
        self.master_key = self._generate_static_key()
        self.data_file = 'passwords.txt'
        self.passwords = self._load_passwords()

    def _generate_static_key(self):
        # Use a fixed salt and password to generate a static key
        salt = b'\x00' * 16
        password = 'static_master_password'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Ensure key length is 256 bits (32 bytes)
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password.encode())

    def _encrypt(self, plaintext):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.master_key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return base64.urlsafe_b64encode(iv + ciphertext).decode()

    def _decrypt(self, ciphertext):
        raw_data = base64.urlsafe_b64decode(ciphertext)
        iv = raw_data[:16]
        cipher = Cipher(algorithms.AES(self.master_key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(raw_data[16:]) + decryptor.finalize()
        return plaintext.decode(errors='ignore')  

    def _load_passwords(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                encrypted_data = f.read()
                if encrypted_data:
                    try:
                        decrypted_data = self._decrypt(encrypted_data)
                        return json.loads(decrypted_data)
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        return {}
        return {}

    def _save_passwords(self):
        with open(self.data_file, 'wb') as f:
            encrypted_data = self._encrypt(json.dumps(self.passwords))
            f.write(encrypted_data.encode())

    def add_password(self, category, identifier, password):
        if category not in self.passwords:
            self.passwords[category] = {}
        self.passwords[category][identifier] = password
        self._save_passwords()

    def get_password(self, category, identifier):
        return self.passwords.get(category, {}).get(identifier)

    def generate_strong_password(self, length=16):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+="
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    def calculate_password_strength(self, password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()-_+=" for c in password)

        strength = 0
        if length >= 8:
            strength += 25
        if has_upper:
            strength += 25
        if has_lower:
            strength += 25
        if has_digit:
            strength += 15
        if has_symbol:
            strength += 10

        return min(strength, 100)

# Function to prompt the user for input and suggest a password
def prompt_user_for_credentials(pm):
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")

    suggested_password = pm.generate_strong_password()
    print(f"Suggested password: {suggested_password}")

    password_choice = input("Do you want to use the suggested password? (yes/no): ")
    if password_choice.lower() == 'yes':
        password = suggested_password
    else:
        password = input("Enter your desired password: ")

    return first_name, last_name, email, password

# Example usage
pm = PasswordManager()

# Prompt user for credentials
first_name, last_name, email, password = prompt_user_for_credentials(pm)

# Print user's name
print(f"User: {first_name} {last_name}")

# Calculate and display password strength
password_strength = pm.calculate_password_strength(password)
print(f"Password strength: {password_strength}%")

# Add the password under the category "User Accounts" and identifier as email
category = "User Accounts"
identifier = email
pm.add_password(category, identifier, password)
print(f"Password for {identifier} in {category} added successfully.")


