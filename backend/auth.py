import os
import secrets
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def authenticate_admin(username: str, password: str):
    admin_user = os.environ.get("ADMIN_USERNAME")
    admin_pass = os.environ.get("ADMIN_PASSWORD")

    if not admin_user or not admin_pass:
        logger.error("ADMIN_USERNAME or ADMIN_PASSWORD environment variables are missing.")
        raise HTTPException(status_code=500, detail="Server misconfiguration: Authentication not set up")

    # Secure string comparison to prevent timing attacks
    is_user_correct = secrets.compare_digest(username.encode("utf-8"), admin_user.encode("utf-8"))
    is_pass_correct = secrets.compare_digest(password.encode("utf-8"), admin_pass.encode("utf-8"))

    if not (is_user_correct and is_pass_correct):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
