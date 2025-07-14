#Import's Modules
import tkinter as tk
from tkinter import messagebox
import json # Import the json module to handle reading and writing data in JSON format
import pyperclip # Import pyperclip to enable copying text (like passwords) to the system clipboard
import sys # Used to access interpreter-specific variables (like _MEIPASS when using PyInstaller)
import os # Used for file path and directory handling
from core.crypto_util import Encryptor 
from core.password_logic import PasswordGenerator

# Define a function to get the absolute path to a resource file
def resource_path(relative_path):
    """ 
    Get the absolute path to a resource file.
    This allows the app to locate files (like icons or data) whether it's being run as a .py script 
    OR as a bundled .exe created by PyInstaller.
    PyInstaller extracts all files to a temporary directory at runtime (stored in sys._MEIPASS),
    so we use that if available. Otherwise, fall back to the current working directory.  
    """
    try:
        base_path = sys._MEIPASS  # When running as a bundled .exe, PyInstaller sets this to the temp path
    except AttributeError:
        base_path = os.path.abspath(".") # When running from source (.py), use the current directory
    
    # Join the base path with the relative file path and return the full absolute path
    return os.path.join(base_path, relative_path)

# Create a writable app data folder for saving JSON and keys
# Get the path to the user's AppData\Roaming folder (e.g., C:\Users\YourName\AppData\Roaming) 
# and append 'VaultKey' to create a unique directory for this app
APP_DIR = os.path.join(os.getenv("APPDATA"), "VaultKey")

#Create the VaultKey directory if it doesn't already exist
#'exist_ok=True' prevents an error if the folder is already present
os.makedirs(APP_DIR, exist_ok=True)

# Define the full path where the encrypted password data will be stored
USER_DATA_PATH = os.path.join(APP_DIR, "password_data.json")

# Define the full path where the secret encryption key will be stored
USER_KEY_PATH = os.path.join(APP_DIR, "secret.key")



#Create Class
class PasswordManager():
    def __init__(self, root):
        self.root = root
        self.password_generator = PasswordGenerator()  #Creating object
        self.encryptor = Encryptor()

        #Setup Screen
        self.root.title("Password Manager")
        self.root.config(padx=20, pady=20)
        self.root.resizable(False, False)
        self.dark_mode = True  # Start in dark mode by default
        
        self.sun_icon = tk.PhotoImage(file=resource_path("assets/sun.png")) # Light mode icon
        self.moon_icon = tk.PhotoImage(file=resource_path("assets/moon.png")) # Dark mode icon

        self.setup_ui()

    #Setup User Interface
    def setup_ui(self):
        #Setup Image on Screen
        canva = tk.Canvas(width=200, height=200, highlightthickness=0)  #Setup Canva Screen & Remove border
        logo_image = tk.PhotoImage(file=resource_path("assets/logo.png")) #Take Image
        canva.create_image(100, 100, image=logo_image) #Display Image on Screen 
        canva.grid(row=0, column=1)
        self.logo_image = logo_image  # prevent garbage collection

        #Setup UI
        tk.Label(text="Website: ").grid(row=1, column=0) #Set website text
        tk.Label(text="Email/Username: ").grid(row=2, column=0, pady=5) #Set user text
        tk.Label(text="Password: ").grid(row=3, column=0) #Set password text

        self.website_entry = tk.Entry(width=26) #Set Website Entry box
        self.website_entry.grid(row=1, column=1)
        self.website_entry.focus()

        self.email_entry = tk.Entry(width=45) #Set user entry box
        self.email_entry.grid(row=2, column=1, columnspan=2)

        self.password_entry = tk.Entry(width=26) #Set password entry box
        self.password_entry.grid(row=3, column=1) 

        tk.Button(text="Generate Password", command=self.generate).grid(row=3, column=2) #Set Generate Button
        tk.Button(text="Add", width=40, command=self.save_password).grid(row=4, column=1, columnspan=2, pady=10) #Set Add Button
        tk.Button(text="Search", width=15, command=self.search).grid(row=1, column=2) #Set Search Button
        
        self.theme_button = tk.Button(image=self.moon_icon, command=self.toggle_theme, bd=0, highlightthickness=0)
        self.theme_button.grid(row=4, column=3, pady=5)

        self.apply_theme()  # Apply the initial theme (dark by default)

    #Theme of App
    def apply_theme(self):
        if self.dark_mode:
            self.bg_color = "#2e2e2e"
            self.fg_color = "#ffffff"
            self.entry_bg = "#3c3f41"
            self.button_bg = "#5c5c5c"
        else:
            self.bg_color = "#f0f0f0"
            self.fg_color = "#000000"
            self.entry_bg = "#ffffff"
            self.button_bg = "#e0e0e0"

        self.root.configure(bg=self.bg_color)

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=self.bg_color, fg=self.fg_color)
            elif isinstance(widget, tk.Entry):
                widget.config(bg=self.entry_bg, fg=self.fg_color, insertbackground=self.fg_color)
            elif isinstance(widget, tk.Button):
                widget.config(bg=self.button_bg, fg=self.fg_color,
                            activebackground="#d0d0d0" if not self.dark_mode else "#4d4d4d",
                            activeforeground=self.fg_color)
            elif isinstance(widget, tk.Canvas):
                widget.config(bg=self.bg_color, highlightthickness=0)

    #Change the Theme
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode  # Switch mode
        self.theme_button.config(image=self.moon_icon if self.dark_mode else self.sun_icon)
        self.apply_theme()  # Apply the selected theme

    #Generate Password
    def generate(self):
        password = self.password_generator.generate_password()
        pyperclip.copy(password) #Copy password in keybord
        self.password_entry.delete(0, tk.END) #Clean password field
        self.password_entry.insert(0, password) #Insert password in password field

    #Save details in File
    def save_password(self):
        website = self.website_entry.get().capitalize() #Get Website name
        email = self.email_entry.get() #Get Username/Email 
        new_password = self.encryptor.encrypt(self.password_entry.get())  # Encrypt Password

        #Set data as Dictionary
        new_data = {
            website: {
                "Email": email,
                "Password": new_password
            }
        }

        if len(website) == 0 or len(email) == 0 or len(new_password) == 0: #Check any field is empty or not
            #Display the messagebox to show user the filed is empty 
            messagebox.showinfo(title="Oops", message="Please don't leave any field Empty!") 
            return
        
        # First-time setup: check if the writable password data file exists
        if not os.path.exists(USER_DATA_PATH):
            try:
                # Try to open the bundled read-only asset file inside the .exe or source folder
                with open(resource_path("assets/password_data.json"), "r") as src:
                    # Create a new writable copy in AppData (or overwrite if needed)
                    with open(USER_DATA_PATH, "w") as dst:
                        dst.write(src.read())  # Copy contents from bundled file to AppData
            except FileNotFoundError:
                # If the bundled asset file doesn't exist, create an empty JSON file in AppData
                with open(USER_DATA_PATH, "w") as f:
                    f.write("{}")  # Start with an empty dictionary as JSON content

        try:
            with open(USER_DATA_PATH, "r") as data_file: #Open Json file in Read mode
                data = json.load(data_file) #Read data from json file
        except (FileNotFoundError, json.JSONDecodeError): #If file not found or Empty
            data = {} #It starts with a blank dictionary.

        #Update data with new data 
        data.update(new_data) #If the website already exists, it overwrites the old entry with the new one.

        #Saves the updated data dictionary back to password_data.json.
        with open(USER_DATA_PATH, "w") as data_file: 
            json.dump(data, data_file, indent=4) # Formatting it nicely (indent=4)

        #Clears all fields for the next entry.
        self.website_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.website_entry.focus()  # Automatically puts the cursor back in the website field.

        #Shows a message to confirm the data was saved.
        messagebox.showinfo(title="Success", message="Data successfully stored!")

    #Search Details in file
    def search(self):
        website = self.website_entry.get().capitalize() #Get Website name
        
        if len(website) == 0: #Check the website filed is empty or not
            messagebox.showwarning(title="Warning", message="Website field is empty.")
            return
        
        # First-time setup: check if the writable password data file exists
        if not os.path.exists(USER_DATA_PATH):
            try:
                # Try to open the bundled read-only asset file inside the .exe or source folder
                with open(resource_path("assets/password_data.json"), "r") as src:
                    # Create a new writable copy in AppData (or overwrite if needed)
                    with open(USER_DATA_PATH, "w") as dst:
                        dst.write(src.read())  # Copy contents from bundled file to AppData
            except FileNotFoundError:
                # If the bundled asset file doesn't exist, create an empty JSON file in AppData
                with open(USER_DATA_PATH, "w") as f:
                    f.write("{}")  # Start with an empty dictionary as JSON content

        try:
            with open(USER_DATA_PATH, "r") as data_file: #Open Json file in Read mode
                data = json.load(data_file) #Read data from json file 
                email = data[website]["Email"] #Get email from data
                encrypted_pw = data[website]["Password"]
                password = self.encryptor.decrypt(encrypted_pw) #Get password from data
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}") #Show search result in messagebox
        except FileNotFoundError: #IF file not found then create it
            open(USER_DATA_PATH, "w") #Open Json file in Write mode
        except json.JSONDecodeError: #If File is empty 
            messagebox.showerror(title="Error", message="File is empty or corrupted.") #Show File is empty or corrupted in messagebox
        except KeyError: #Website not in file
            messagebox.showinfo(title="Not Found", message=f"No details for {website}") #Show website not found in messagebox


if __name__ == "__main__":
    root = tk.Tk()
    PasswordManager(root)
    root.mainloop()