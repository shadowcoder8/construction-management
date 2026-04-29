import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    # Secure authentication logic using environment variables
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    if not secrets.compare_digest(username, admin_username) or not secrets.compare_digest(password, admin_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
