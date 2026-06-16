import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_user = os.getenv("ADMIN_USERNAME")
    admin_pass = os.getenv("ADMIN_PASSWORD")

    if not admin_user or not admin_pass:
        raise HTTPException(status_code=500, detail="Admin credentials not configured")

    is_user_ok = secrets.compare_digest(username.encode('utf-8'), admin_user.encode('utf-8'))
    is_pass_ok = secrets.compare_digest(password.encode('utf-8'), admin_pass.encode('utf-8'))

    if not (is_user_ok and is_pass_ok):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
