import os
import secrets
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

def authenticate_admin(username: str, password: str):
    admin_user = os.environ.get('ADMIN_USERNAME')
    admin_pass = os.environ.get('ADMIN_PASSWORD')

    if not admin_user or not admin_pass:
        logger.error("Admin credentials are not configured in environment variables")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Use compare_digest to prevent timing attacks
    # Ensure both string lengths are verified without short-circuiting to prevent leaking info
    is_user_correct = secrets.compare_digest(username, admin_user)
    is_pass_correct = secrets.compare_digest(password, admin_pass)

    if not (is_user_correct and is_pass_correct):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
