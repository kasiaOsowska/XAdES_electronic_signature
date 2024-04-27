from threading import Thread
import psutil
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import config

file_path = None
def find_pendrive_path_windows():
    for device in psutil.disk_partitions():
        if 'removable' in device.opts:
            return device.mountpoint
    return None


def pendrive_detection(window):
    window.console.append("Oczekiwanie na pendrive...")
    while True:
        pendrive_path = find_pendrive_path_windows()
        if pendrive_path:
            window.console.append(f"Pendrive znaleziony w ścieżce: {pendrive_path}")
            return pendrive_path


def decrypt_key_async(window):
    thread = Thread(target=find_file, args=(window,))
    thread.start()


def find_file(second_window):
    global file_path
    path = pendrive_detection(second_window)
    file_name = "encrypted_private_key.bin"
    file_path = Path(path + file_name)
    if not file_path.is_file():
        second_window.console.append("Nie znaleziono pliku z kluczem na pendrive")
    else:
        second_window.console.append("Znaleziono plik z kluczem na pendrive")


def decrypt_key(second_window):

    with open(file_path, "rb") as f:
        encrypted_private_key = f.read()

    second_window.console.append("Wprowadź PIN: ")
    pin = second_window.get_PIN()
    hasher = SHA256.new()
    hasher.update(pin.encode())
    key = hasher.digest()
    try:
        decipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = unpad(decipher.decrypt(encrypted_private_key), AES.block_size)

        print(f'Zaszyfrowane dane: {encrypted_private_key}')
        print(f'Odszyfrowane dane: {decrypted_data}')

        loaded_private_key = load_pem_private_key(
            decrypted_data,
            password=None,
            backend=default_backend()
        )
        second_window.console.append("Klucz prywatny został pomyślnie odszyfrowany i załadowany.")
        second_window.console.append("Możesz zamknąć to okno")
    except Exception as e:
        second_window.console.append(f"Wystąpił błąd podczas deszyfrowania klucza, możliwe, że podałeś zły PIN: {e}")
        second_window.console.append("Spróbuj jeszcze raz")
        return None

    config.PRIVATE_KEY = loaded_private_key
