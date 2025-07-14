from cryptography.fernet import Fernet
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource (works for PyInstaller .exe) """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this at runtime
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Create a writable app data folder for saving JSON and keys
APP_DIR = os.path.join(os.getenv("APPDATA"), "VaultKey")
os.makedirs(APP_DIR, exist_ok=True)

USER_DATA_PATH = os.path.join(APP_DIR, "password_data.json")
USER_KEY_PATH = os.path.join(APP_DIR, "secret.key")

KEY_PATH = USER_KEY_PATH

def generate_key():
    os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_PATH):
        generate_key()
    with open(KEY_PATH, "rb") as f:
        return f.read()

class Encryptor:
    def __init__(self):
        self.key = load_key()
        self.fernet = Fernet(self.key)

    def encrypt(self, message: str) -> str:
        return self.fernet.encrypt(message.encode()).decode()

    def decrypt(self, encrypted_message: str) -> str:
        return self.fernet.decrypt(encrypted_message.encode()).decode()
