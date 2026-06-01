import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    expected_username = os.environ.get("ADMIN_USERNAME")
    expected_password = os.environ.get("ADMIN_PASSWORD")

    if not expected_username or not expected_password:
        raise HTTPException(status_code=500, detail="Admin credentials are not configured on the server")

    if not (secrets.compare_digest(username, expected_username) and secrets.compare_digest(password, expected_password)):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
