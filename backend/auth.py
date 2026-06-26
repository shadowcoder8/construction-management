import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_username = os.environ.get("ADMIN_USERNAME")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Use secrets.compare_digest with utf-8 encoding to prevent timing attacks
    # and handle non-ASCII characters correctly.
    is_username_valid = secrets.compare_digest(username.encode("utf-8"), admin_username.encode("utf-8"))
    is_password_valid = secrets.compare_digest(password.encode("utf-8"), admin_password.encode("utf-8"))

    if not (is_username_valid and is_password_valid):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
