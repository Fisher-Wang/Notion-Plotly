import argparse
import os

from utils import (
    encrypt_file,
    generate_item_id,
    generate_key_id,
    get_all_files,
    mkdir,
    read_toml,
)

conf = read_toml("config.toml")
src_dir = conf["directory"]["plaintext_dir"]
dst_dir = conf["directory"]["encrypted_dir"]
key_dir = conf["directory"]["key_dir"]

mkdir(dst_dir)
mkdir(key_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    records = []
    src_filepaths = get_all_files(src_dir)
    for src_filepath in src_filepaths:
        file_name = os.path.basename(src_filepath)
        file_id = generate_item_id(file_name)
        key_id = generate_key_id(file_name)
        dst_filepath = os.path.join(dst_dir, file_id)
        key_filepath = os.path.join(key_dir, key_id)

        # If the file already exists, use the existing key; otherwise, generate a new key and save it
        if os.path.exists(dst_filepath):
            key = open(key_filepath, "rb").read()
            encrypt_file(src_filepath, dst_filepath, key=key)
        else:
            key = encrypt_file(src_filepath, dst_filepath)
            with open(key_filepath, "wb") as f:
                f.write(key)

        records.append(
            {
                "src_filepath": src_filepath,
                "dst_filepath": dst_filepath,
                "key": key,
                "url": f'https://mac.robofisher.xyz/html/{file_id}?k={key.decode("utf-8")}',
            }
        )

    print(records)
