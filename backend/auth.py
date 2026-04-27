import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    # Fetch admin credentials from environment variables
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

    # Use secrets.compare_digest to prevent timing attacks
    is_username_correct = secrets.compare_digest(username, admin_username)
    is_password_correct = secrets.compare_digest(password, admin_password)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
