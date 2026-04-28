from fastapi import HTTPException
import os
import secrets

def authenticate_admin(username: str, password: str):
    # Dummy authentication logic
    expected_username = os.environ.get("ADMIN_USERNAME", "admin")
    expected_password = os.environ.get("ADMIN_PASSWORD", "admin123")

    if not (secrets.compare_digest(username, expected_username) and secrets.compare_digest(password, expected_password)):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
