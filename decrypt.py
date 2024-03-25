from cryptography.fernet import Fernet

def decrypt_message(ciphertext, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(ciphertext)
    return decrypted_message

def main():
    # Utilisez une clé existante ou générez une nouvelle clé
    key = input("Entrez la clé de chiffrement : ").encode('utf-8')  # Assurez-vous que la clé est encodée en bytes

    ciphertext = input("Entrez le message chiffré :").encode('utf-8')  # Assurez-vous que le texte chiffré est en bytes

    decrypted_message = decrypt_message(ciphertext, key)
    print("Message déchiffré :", decrypted_message.decode('utf-8'))

if __name__ == "__main__":
    main()
