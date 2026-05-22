from fastapi import HTTPException
import os
import secrets

def authenticate_admin(username: str, password: str):
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Admin credentials not configured")

    if not secrets.compare_digest(username, admin_username) or \
       not secrets.compare_digest(password, admin_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
