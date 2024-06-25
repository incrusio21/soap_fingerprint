from cryptography.fernet import Fernet

fernet_key = Fernet("NdMs3c8omCpfMIaIAyq0bTYP0uPU0IaGhllqfjRTVsU=")

def get_key():
    return Fernet.generate_key()

