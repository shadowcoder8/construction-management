import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_user = os.environ.get("ADMIN_USERNAME")
    admin_pass = os.environ.get("ADMIN_PASSWORD")

    if not admin_user or not admin_pass:
        # Securely fail if configuration is missing, avoiding unauth access
        raise HTTPException(status_code=500, detail="Admin credentials not configured")

    # Use secrets.compare_digest to prevent timing attacks
    is_user_valid = secrets.compare_digest(username, admin_user)
    is_pass_valid = secrets.compare_digest(password, admin_pass)

    if not (is_user_valid and is_pass_valid):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
