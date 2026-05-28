import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    expected_username = os.environ.get("ADMIN_USERNAME")
    expected_password = os.environ.get("ADMIN_PASSWORD")

    if expected_username is None or expected_password is None:
        raise HTTPException(status_code=500, detail="Admin credentials are not configured on the server")

    if not secrets.compare_digest(username, expected_username) or not secrets.compare_digest(password, expected_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
