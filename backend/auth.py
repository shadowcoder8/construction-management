from fastapi import HTTPException

def authenticate_admin(username: str, password: str):
    # Dummy authentication logic
    if username != "admin" or password != "admin123":
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}
