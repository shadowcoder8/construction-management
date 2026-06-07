import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    env_username = os.getenv("ADMIN_USERNAME")
    env_password = os.getenv("ADMIN_PASSWORD")

    if not env_username or not env_password:
        raise HTTPException(status_code=500, detail="Server configuration error")

    username_match = secrets.compare_digest(username.encode("utf-8"), env_username.encode("utf-8"))
    password_match = secrets.compare_digest(password.encode("utf-8"), env_password.encode("utf-8"))

    if not (username_match and password_match):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
