from fastapi import HTTPException
import os
import secrets

def authenticate_admin(username: str, password: str):
    admin_username = os.environ.get("ADMIN_USERNAME")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Admin credentials are not configured properly")

    is_correct_username = secrets.compare_digest(username.encode("utf-8"), admin_username.encode("utf-8"))
    is_correct_password = secrets.compare_digest(password.encode("utf-8"), admin_password.encode("utf-8"))

    if not (is_correct_username and is_correct_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
