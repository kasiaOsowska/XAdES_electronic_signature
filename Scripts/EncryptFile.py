from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Scripts.EncryptDecryptFunctions import get_file_metadata
import os
import config


def encrypt_file_with_public_key(file_path, window):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = config.PUBLIC_KEY.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        window.appendText("Błąd podczas szyfrowania pliku: " + str(e))
        return None
    return encrypted_data


def decrypt_file_wirh_private_key(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    decrypted_data = config.PRIVATE_KEY.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data


def decrypt(file_path, window):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    data = decrypt_file_wirh_private_key(file_path)
    if data is None:
        return
    decrypted_file_path = os.path.join(os.path.dirname(file_path), f"{file_name}_dec")
    with open(decrypted_file_path, 'wb') as f:
        f.write(data)
    window.appendText(f"Odszyfrowany plik znajduje się w: {file_path}")
    return


def encrypt(file_path, window):
    file_stats = os.stat(file_path)
    size = file_stats.st_size
    if size < 5120:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        data = encrypt_file_with_public_key(file_path, window)
        if data is None:
            return
        encrypted_file_path = os.path.join(os.path.dirname(file_path), f"{file_name}_enc.bin")
        with open(encrypted_file_path, 'wb') as f:
            f.write(data)
        window.appendText(f"Zaszyfrowany plik znajduje się w: {file_path}")
    else:
        window.appendText("Plik jest zbyt duży, aby go zaszyfrować")
        return
