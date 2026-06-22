import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Admin credentials not configured")

    username_match = secrets.compare_digest(username.encode("utf-8"), admin_username.encode("utf-8"))
    password_match = secrets.compare_digest(password.encode("utf-8"), admin_password.encode("utf-8"))

    if not (username_match and password_match):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
