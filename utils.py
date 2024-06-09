import hashlib
import os

import toml
from cryptography.fernet import Fernet


def mkdir(path):
    """Create a directory if it does not exist."""
    os.makedirs(path, exist_ok=True)
    return path


def read_toml(path):
    """Read a TOML file and return the data."""
    with open(path) as f:
        data = toml.load(f)
    return data


def get_all_files(src_dir):
    filepaths = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            filepaths.append(os.path.join(root, file))
    return filepaths


def generate_item_id(file_name):
    """Generate a unique item ID for a file based on its name."""
    return hashlib.md5(file_name.encode("utf-8")).hexdigest()


def generate_key_id(file_name):
    """Generate a unique key ID for a file based on its name."""
    return hashlib.sha256(file_name.encode("utf-8")).hexdigest()


def encrypt_data(data, key=None):
    if key is None:
        key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    return encrypted_data, key


def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data


def encrypt_file(src_filepath, dst_filepath, key=None):
    with open(src_filepath, "rb") as f:
        data = f.read()
    encrypted_data, key = encrypt_data(data, key=key)
    with open(dst_filepath, "wb+") as f:
        f.write(encrypted_data)
    return key
