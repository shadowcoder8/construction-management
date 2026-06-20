from fastapi import HTTPException

import os
import secrets

def authenticate_admin(username: str, password: str):
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Admin credentials are not configured")

    is_user_valid = secrets.compare_digest(username.encode('utf-8'), admin_username.encode('utf-8'))
    is_pass_valid = secrets.compare_digest(password.encode('utf-8'), admin_password.encode('utf-8'))

    if not (is_user_valid and is_pass_valid):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
