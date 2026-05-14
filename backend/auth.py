from fastapi import HTTPException
import os
import secrets
import logging

logger = logging.getLogger(__name__)

def authenticate_admin(username: str, password: str):
    expected_username = os.getenv("ADMIN_USERNAME")
    expected_password = os.getenv("ADMIN_PASSWORD")

    if not expected_username or not expected_password:
        logger.error("ADMIN_USERNAME or ADMIN_PASSWORD environment variables are not set")
        raise HTTPException(status_code=500, detail="Internal server configuration error")

    # Use secrets.compare_digest to prevent timing attacks
    is_username_correct = secrets.compare_digest(username, expected_username)
    is_password_correct = secrets.compare_digest(password, expected_password)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
