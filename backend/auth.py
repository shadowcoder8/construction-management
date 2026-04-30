from fastapi import HTTPException
import os
import secrets

def authenticate_admin(username: str, password: str):
    # Ensure credentials are provided securely via environment variables
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    # Fail securely if environment variables are not set
    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Server configuration error")

    # Use secrets.compare_digest for constant-time comparison to prevent timing attacks
    if not secrets.compare_digest(username, admin_username) or not secrets.compare_digest(password, admin_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
