from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import config
import os
import pathlib
import win32security
import datetime


def sign_hash(hash_value):
    signature = config.PRIVATE_KEY.sign(
        hash_value,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def hash_document(file_path):
    hasher = hashes.Hash(hashes.SHA256(), backend=default_backend())
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.finalize()


def verify_signature(signature, hash_value, window):
    try:
        config.PUBLIC_KEY.verify(
            signature,
            hash_value,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        window.appendText("Podpis jest poprawny, dokument nie był modyfikowany")
    except InvalidSignature:
        window.appendText("Nieprawidłowy podpis: Skróty nie zgadzają się.")
    except Exception as e:
        window.appendText("Błąd weryfikacji podpisu:" + str(e))


def get_file_metadata(file_path):
    file_stats = os.stat(file_path)
    last_modified_epoch = file_stats.st_mtime
    last_modified = datetime.datetime.utcfromtimestamp(last_modified_epoch).isoformat()
    size = file_stats.st_size
    extension = pathlib.Path(file_path).suffix

    if os.name == 'nt':
        security_info = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = security_info.GetSecurityDescriptorOwner()
        owner_name, _, _ = win32security.LookupAccountSid(None, owner_sid)
        file_owner = owner_name
    else:
        file_owner = None

    return {
        "last_modified": str(last_modified),
        "size": str(size) + "B",
        "extension": str(extension),
        "author": str(file_owner)
    }


def Load_public_key(key_path, window):
    with open(key_path, "rb") as f:
        pem_public_key = f.read()
    try:
        config.PUBLIC_KEY = serialization.load_pem_public_key(pem_public_key, backend=default_backend())
        window.appendText("Klucz publiczny został wczytany")
    except Exception as e:
        window.appendText("Błąd podczas wczytywania klucza publicznego")
        window.appendText(str(e))