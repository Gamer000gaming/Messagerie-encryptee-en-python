from cryptography.fernet import Fernet
import json
import os
import base64
import tkinter as tk
from tkinter import messagebox

def generate_key():
    k = Fernet.generate_key()
    if not os.path.exists("key.txt"):
        keyf = open("key.txt", "wb")
        keyf.write(k)
        keyf.close()

def encrypt(message, key):
    cipher_suite = Fernet(key)
    ciphertext = cipher_suite.encrypt(message)
    return ciphertext

def decrypt(ciphertext, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(ciphertext)
    return decrypted_message.decode('utf-8')

def create_account():
    username = username_entry.get()
    password = password_entry.get()

    users = load_users()

    if username in users:
        messagebox.showerror("Erreur", "Ce nom d'utilisateur existe déjà.")
        return

    users[username] = {"password": password}
    save_users(users)
    messagebox.showinfo("Succès", "Compte créé avec succès.")

def login():
    username = username_entry.get()
    password = password_entry.get()

    users = load_users()

    if username not in users or users[username]["password"] != password:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        return

    messagebox.showinfo("Succès", "Connexion réussie.")

    # Fermer la fenêtre principale
    main_frame.destroy()

    # Ouvrir la fenêtre de conversation
    conversation_window(username)

def conversation_window(username):
    conversation_frame = tk.Tk()
    conversation_frame.title(f"Conversation - {username}")

    conv_text = tk.Text(conversation_frame)
    conv_text.pack(expand=True, fill=tk.BOTH)

    load_messages(conv_text)  # Charger les messages depuis le fichier de conversation

    msg_entry = tk.Entry(conversation_frame)
    msg_entry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    send_button = tk.Button(conversation_frame, text="Envoyer", command=lambda: send_message(msg_entry.get(), conv_text, username))
    send_button.pack(side=tk.RIGHT)

    refresh_button = tk.Button(conversation_frame, text="Rafraîchir", command=lambda: refresh_messages(conv_text))
    refresh_button.pack(side=tk.RIGHT)

    conversation_frame.mainloop()

def load_messages(conv_text):
    conv = open("conv.txt", "r")
    conv.seek(0)  # Réinitialise la position du curseur au début du fichier de conversation
    for line in conv.readlines():
        decrypted_line = decrypt(base64.urlsafe_b64decode(line), open("key.txt", "rb").read())
        conv_text.insert(tk.END, decrypted_line + '\n')
    conv.close()

def refresh_messages(conv_text):
    conv_text.delete(1.0, tk.END)  # Efface tous les messages actuels dans la fenêtre de conversation
    load_messages(conv_text)  # Recharge les messages depuis le fichier de conversation

def main_window():
    global username_label, username_entry, password_label, password_entry, main_frame
    main_frame = tk.Tk()
    main_frame.title("Programme d'échanges cryptés")

    username_label = tk.Label(main_frame, text="Nom d'utilisateur:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    username_entry = tk.Entry(main_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = tk.Label(main_frame, text="Mot de passe:")
    password_label.grid(row=1, column=0, padx=5, pady=5)

    password_entry = tk.Entry(main_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    create_account_button = tk.Button(main_frame, text="Créer un compte", command=create_account)
    create_account_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    login_button = tk.Button(main_frame, text="Se connecter", command=login)
    login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    main_frame.mainloop()

if not os.path.exists("conv.txt"):
    create = open("conv.txt", "x")
    create.close()

USERS_FILE = "users.json"

# Fonction pour charger les utilisateurs depuis le fichier
def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            users = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        users = {}
    return users

# Fonction pour sauvegarder les utilisateurs dans le fichier
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

def send_message(message, conv_text, username):
    if message == "":
        return
    msg = f"{username} : {message}"
    crypt_msg = base64.urlsafe_b64encode(encrypt(msg.encode('utf-8'), open("key.txt", "rb").read())).decode('utf-8')
    conv_text.insert(tk.END, msg + '\n')  # Ajoute le message à la fenêtre de conversation
    with open("conv.txt", "a") as conv_file:
        conv_file.write(crypt_msg + '\n')  # Ajoute le message au fichier de conversation

if __name__ == "__main__":
    generate_key()
    main_window()
