import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    # Retrieve credentials from environment variables
    admin_username = os.environ.get("ADMIN_USERNAME")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Server configuration error: Admin credentials are not set")

    # Use secure comparison to prevent timing attacks, encoding strings to bytes to handle non-ASCII chars
    is_username_correct = secrets.compare_digest(username.encode("utf-8"), admin_username.encode("utf-8"))
    is_password_correct = secrets.compare_digest(password.encode("utf-8"), admin_password.encode("utf-8"))

    if not (is_username_correct and is_password_correct):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
