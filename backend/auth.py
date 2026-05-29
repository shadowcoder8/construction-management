import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_user = os.environ.get("ADMIN_USERNAME")
    admin_pass = os.environ.get("ADMIN_PASSWORD")

    if not admin_user or not admin_pass:
        raise HTTPException(status_code=500, detail="Server configuration error: Admin credentials are not set")

    if not secrets.compare_digest(username, admin_user) or not secrets.compare_digest(password, admin_pass):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
