import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    is_valid_username = secrets.compare_digest(username, admin_username)
    is_valid_password = secrets.compare_digest(password, admin_password)

    if not (is_valid_username and is_valid_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
