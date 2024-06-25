from cx_Freeze import setup, Executable
from constants import fernet_key


# opening the original file to encrypt
with open('setting.yaml', 'rb') as file:
    original = file.read()

# encrypting the file
encrypted = fernet_key.encrypt(original)
 
# opening the file in write mode and 
# writing the encrypted data
with open('setting', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["unittest", "email"],
    "zip_include_packages": ['constants', "encodings", "PySide6", "shiboken6"],
    "include_files": ["setting"]
}

setup(
    name="Fingerprint SOAP",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("setting.py", base="gui"), Executable("fp_log_data.py", base="gui")],
)