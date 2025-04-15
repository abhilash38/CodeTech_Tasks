from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox

# Generate and save a key (only once)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_file(filepath):
    key = load_key()
    f = Fernet(key)
    with open(filepath, "rb") as file:
        encrypted = f.encrypt(file.read())
    with open(filepath + ".enc", "wb") as enc_file:
        enc_file.write(encrypted)

def decrypt_file(filepath):
    key = load_key()
    f = Fernet(key)
    with open(filepath, "rb") as enc_file:
        decrypted = f.decrypt(enc_file.read())
    new_path = filepath.replace(".enc", "")
    with open(new_path, "wb") as dec_file:
        dec_file.write(decrypted)

# GUI with Tkinter
def browse_file(action):
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    try:
        if action == "encrypt":
            encrypt_file(filepath)
            messagebox.showinfo("Success", "File encrypted successfully.")
        else:
            decrypt_file(filepath)
            messagebox.showinfo("Success", "File decrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
generate_key()
root = tk.Tk()
root.title("AES Encryption Tool")

tk.Label(root, text="Advanced AES-256 Encryption Tool", font=("Helvetica", 14)).pack(pady=10)

tk.Button(root, text="Encrypt File", command=lambda: browse_file("encrypt")).pack(pady=5)
tk.Button(root, text="Decrypt File", command=lambda: browse_file("decrypt")).pack(pady=5)

root.mainloop()
