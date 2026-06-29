from fastapi import HTTPException
import os
import secrets

def authenticate_admin(username: str, password: str):
    # Load credentials from environment variables
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Server configuration error")

    # Securely compare strings using secrets.compare_digest with utf-8 encoding to prevent timing attacks
    is_valid_user = secrets.compare_digest(username.encode("utf-8"), admin_username.encode("utf-8"))
    is_valid_pass = secrets.compare_digest(password.encode("utf-8"), admin_password.encode("utf-8"))

    if not (is_valid_user and is_valid_pass):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
