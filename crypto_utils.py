import os
from cryptography.fernet import Fernet

# Carrega a chave da variável de ambiente
key = os.getenv("ENCRYPTION_KEY")

if not key:
    raise ValueError("Chave de criptografia não encontrada! Defina a variável de ambiente ENCRYPTION_KEY.")

cipher_suite = Fernet(key.encode())

def encrypt_password(password):
    """Criptografa uma senha."""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """Descriptografa uma senha."""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
