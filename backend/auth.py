import os
import secrets
from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise HTTPException(status_code=500, detail="Admin credentials are not configured on the server")

    try:
        is_username_correct = secrets.compare_digest(username.encode("utf-8"), admin_username.encode("utf-8"))
        is_password_correct = secrets.compare_digest(password.encode("utf-8"), admin_password.encode("utf-8"))
    except TypeError:
        # Prevent type errors from non-ascii characters when encoded and compared, just in case
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not (is_username_correct and is_password_correct):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
