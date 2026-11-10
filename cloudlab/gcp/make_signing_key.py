"""Make a throwaway signing key for V4 signed URLs on fake-gcs-server.

The Google Cloud Storage client can only sign a URL with a service account key.
The emulator does not check signatures, so a key made on your laptop is enough.
This key is fake. It works only with the emulator. Never commit it.

Run it from this folder in Git Bash:
    uv run --with cryptography python make_signing_key.py

It writes .signing-key.json next to this script. The cloud lab's .gitignore keeps
that file out of Git.
"""

import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

KEY_FILE = Path(__file__).resolve().with_name(".signing-key.json")


def main() -> None:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    key_info = {
        "type": "service_account",
        "project_id": "fspy-local",
        "private_key_id": "made-on-this-laptop-for-the-emulator-only",
        "private_key": pem,
        "client_email": "local-signer@fspy-local.iam.gserviceaccount.com",
        "client_id": "000000000000000000000",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    KEY_FILE.write_text(json.dumps(key_info, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {KEY_FILE.as_posix()}")
    print("Use this path for GCS_SIGNING_KEY_FILE in your .env. Never commit the file.")


if __name__ == "__main__":
    main()
