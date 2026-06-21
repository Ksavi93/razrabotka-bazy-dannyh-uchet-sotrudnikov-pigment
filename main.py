from db import init_db
from src.auth import open_auth

if __name__ == "__main__":
    init_db()
    open_auth()
