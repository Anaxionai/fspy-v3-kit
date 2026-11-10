"""Create ReelPipe's storage on Azurite (task 20). Run it from reelpipe/ in Git Bash:

    uv run --env-file .env python azure/setup.py

Azurite must be running: `docker compose --profile azure up -d` in the kit's cloudlab/ folder.
"""


def main() -> None:
    """Create the container reelpipe-uploads and set its CORS rules.

    Connect with AZURE_STORAGE_CONNECTION_STRING. The CORS rules allow PUT and GET from
    http://localhost:5173, with any header, so the browser can upload with a SAS URL.
    If the container exists already, keep it, so you can run this script again.
    """
    raise NotImplementedError("TODO(task 20): create the container and set the CORS rules")


if __name__ == "__main__":
    main()
