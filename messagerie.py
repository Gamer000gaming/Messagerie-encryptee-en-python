from cryptography.fernet import Fernet
import json
import os
import base64

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

# Fonction pour créer un compte utilisateur
def create_account(username, password):
    users = load_users()

    if username in users:
        print("Ce nom d'utilisateur existe déjà.")
        return

    users[username] = {"password": password}
    save_users(users)
    print("Compte créé avec succès.")

# Fonction pour se connecter à un compte utilisateur
def login(username, password):
    users = load_users()

    if username not in users or users[username]["password"] != password:
        print("Nom d'utilisateur ou mot de passe incorrect.")
        return None

    print("Connexion réussie.")
    return username

# Fonction principale de l'application
def main():
    generate_key()
    conv = open("conv.txt", "a+")
    while True:
        print("Menu du programme d'échanges cryptés:")
        print("\n1. Créer un compte")
        print("2. Se connecter")
        print("3. Quitter")

        choice = input("Choisissez une option (1/2/3) : ")

        if choice == "1":
            username = input("Entrez le nom d'utilisateur : ")
            password = input("Entrez le mot de passe : ")
            create_account(username, password)
        elif choice == "2":
            username = input("Entrez le nom d'utilisateur : ")
            password = input("Entrez le mot de passe : ")
            user = login(username, password)
            if user:
                print(f"Bienvenue, {user}!")
            while True:
                conv.seek(0)  # Réinitialise la position du curseur au début du fichier de conversation
                for line in conv.readlines():
                    decrypted_line = decrypt(base64.urlsafe_b64decode(line), open("key.txt", "rb").read())
                    print(decrypted_line)
                msg = input("Que voulez-vous envoyer? ")
                if msg == "q": break
                elif msg != "":
                    msg = f"{username} : {msg}"
                    crypt_msg = base64.urlsafe_b64encode(encrypt(msg.encode('utf-8'), open("key.txt", "rb").read())).decode('utf-8')

                    conv.write(crypt_msg + '\n')  # Ajoutez un retour à la ligne entre chaque message
                
        elif choice == "3":
            print("Au revoir !")
            break
        else:
            print("Option non valide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
