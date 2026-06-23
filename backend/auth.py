import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_user = os.environ.get("ADMIN_USERNAME")
    admin_pass = os.environ.get("ADMIN_PASSWORD")

    if not admin_user or not admin_pass:
        raise HTTPException(status_code=500, detail="Admin credentials are not configured")

    is_valid_user = secrets.compare_digest(username.encode("utf-8"), admin_user.encode("utf-8"))
    is_valid_pass = secrets.compare_digest(password.encode("utf-8"), admin_pass.encode("utf-8"))

    if not (is_valid_user and is_valid_pass):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
