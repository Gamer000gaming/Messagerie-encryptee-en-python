from cryptography.fernet import Fernet
from tkinter.messagebox import askyesno

def generate_key():
    if askyesno("Clé de chiffrement", "Voulez-vous générer une nouvelle clé?"):
        return Fernet.generate_key()
    else:
        return input("Entrez votre clé ici: ")

def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    ciphertext = cipher_suite.encrypt(message)
    return ciphertext

def main():
    # Génération automatique de la clé
    key = generate_key()
    print("Clé de chiffrement générée :", key)

    plaintext = input("Entrez le message à chiffrer : ").encode('utf-8')

    ciphertext = encrypt_message(plaintext, key)
    print("Message chiffré :", ciphertext)

if __name__ == "__main__":
    main()
