import os

from flask import Flask, Response, abort, request

from utils import decrypt_data, read_toml

conf = read_toml("config.toml")
ENCRYPTED_FOLDER = conf["directory"]["encrypted_dir"]
PORT = conf["server"]["port"]

app = Flask(__name__)


@app.route("/html/<item_id>", methods=["GET"])
def get_file(item_id):
    key = request.args.get("k")
    if not key:
        return {"error": "No key provided"}, 400

    try:
        file_path = os.path.join(ENCRYPTED_FOLDER, item_id)
        if not os.path.exists(file_path):
            return {"error": "File not found"}, 404

        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = decrypt_data(encrypted_data, key.encode("utf-8"))

        return Response(decrypted_data, mimetype="text/html")

    except Exception as e:
        print(f"Error: {e}")
        return abort(404)


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
