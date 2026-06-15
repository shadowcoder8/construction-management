from fastapi import HTTPException
import os
import secrets

def authenticate_admin(username: str, password: str):
    admin_user = os.environ.get("ADMIN_USERNAME")
    admin_pass = os.environ.get("ADMIN_PASSWORD")

    if not admin_user or not admin_pass:
        raise HTTPException(status_code=500, detail="Admin credentials are not configured")

    is_user_valid = secrets.compare_digest(username.encode('utf-8'), admin_user.encode('utf-8'))
    is_pass_valid = secrets.compare_digest(password.encode('utf-8'), admin_pass.encode('utf-8'))

    if not (is_user_valid and is_pass_valid):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
