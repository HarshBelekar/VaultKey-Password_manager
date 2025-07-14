# 🔐 Password Manager App `VaultKey`

A sleek and secure desktop password manager called `VaultKey` — with encryption, dark/light mode toggle, clipboard support, and more.

---

# ✨ Features

- 🌙 **Dark Mode & Light Mode** toggle with icon-based switch (🌞 / 🌚)
- 🔐 **AES Encryption** using `cryptography` to securely store passwords
- 🎲 **Strong Password Generator** (letters, symbols, numbers)
- 🔎 **Search Functionality** to retrieve saved credentials by website
- 💾 **Local JSON Storage** (encrypted)
- 📋 **Clipboard Copy** for generated passwords
- 🖼️ Polished **Tkinter GUI** with custom icons and colors
- 💻 Fully compatible with **PyInstaller** for `.exe` packaging

---

## 📸 Screenshots

| Dark Mode                        | Light Mode                         |
|----------------------------------|------------------------------------|
| ![Dark](assets/dark_preview.png) | ![Light](assets/light_preview.png) |

---

## 🗂️ Folder Structure

    password_manager/
    ├── main.py # Main GUI and app logic
    ├── core/
    │ ├── password_logic.py # PasswordGenerator class
    │ └── crypto_util.py # Encryptor class for encryption/decryption
    ├── assets/
    │ ├── logo.png # App logo
    │ ├── sun.png # Light mode icon
    │ ├── moon.png # Dark mode icon
    │ ├── password_data.json # Encrypted password storage (ignored by git)
    │ └── secret.key # Encryption key (ignored by git)
    ├── requirements.txt # Python dependencies
    ├── README.md # You're reading it!
    └── .gitignore # Prevents sensitive files from being tracked

---

# 🚀 Getting Started

### 1. Clone the repository
    git clone https://github.com/HarshBelekar/Password-Manager.git
    cd password-manager

### 2. Install dependencies
    pip install -r requirements.txt

### 3. Run the app
    python main.py

---

# 🛠 Technologies Used

 -  **tkinter** — GUI framework
 -  **pyperclip** — Clipboard integration
 -  **cryptography** — AES encryption for password security
 -  **json** — Data storage format

---

# 🧪 Build Executable (Windows)

 - Use PyInstaller to convert the app into a standalone executable:

python -m PyInstaller --onefile --windowed --icon=assets/logo.ico --add-data "assets;assets" --name VaultKey main.py

👉 The .exe file will be located in the dist/ folder after the build.

---

# 🛡️ Security Notes

 - Passwords are encrypted using a secure Fernet key, stored in assets/secret.key.

 - Both assets/password_data.json and assets/secret.key are ignored from Git tracking using .gitignore to protect your sensitive data.

# 📦 Future Improvements

 - ✅ Export/import encrypted backups

 - ✅ Add master password authentication

 - ✅ Add support for cloud sync or database-based storage (optional)

---
