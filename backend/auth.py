from fastapi import HTTPException
import os
import secrets

def authenticate_admin(username: str, password: str):
    admin_user = os.getenv("ADMIN_USERNAME")
    admin_pass = os.getenv("ADMIN_PASSWORD")

    if not admin_user or not admin_pass:
        raise HTTPException(status_code=500, detail="Admin credentials not configured in environment")

    is_valid_username = secrets.compare_digest(username, admin_user)
    is_valid_password = secrets.compare_digest(password, admin_pass)

    if not (is_valid_username and is_valid_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
