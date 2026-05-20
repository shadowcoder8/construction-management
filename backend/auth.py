import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_user = os.environ.get("ADMIN_USERNAME")
    admin_pass = os.environ.get("ADMIN_PASSWORD")

    if not admin_user or not admin_pass:
        raise HTTPException(status_code=500, detail="Server misconfiguration: missing admin credentials.")

    is_correct_username = secrets.compare_digest(username, admin_user)
    is_correct_password = secrets.compare_digest(password, admin_pass)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
