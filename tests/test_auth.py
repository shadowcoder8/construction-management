import os
import sys
from fastapi import HTTPException

# Add current directory to path so it can find backend module
sys.path.append(os.getcwd())

from backend.auth import authenticate_admin

def test_auth():
    print("Testing missing credentials...")
    # Ensure they are not set
    if "ADMIN_USERNAME" in os.environ:
        del os.environ["ADMIN_USERNAME"]
    if "ADMIN_PASSWORD" in os.environ:
        del os.environ["ADMIN_PASSWORD"]

    try:
        authenticate_admin("admin", "admin123")
        assert False, "Should have raised 500 HTTPException"
    except HTTPException as e:
        assert e.status_code == 500
        print("Missing credentials test passed.")

    print("Testing valid credentials...")
    os.environ["ADMIN_USERNAME"] = "secureadmin"
    os.environ["ADMIN_PASSWORD"] = "securepass123"

    result = authenticate_admin("secureadmin", "securepass123")
    assert result == {"message": "Login successful"}
    print("Valid credentials test passed.")

    print("Testing invalid credentials...")
    try:
        authenticate_admin("secureadmin", "wrongpass")
        assert False, "Should have raised 401 HTTPException"
    except HTTPException as e:
        assert e.status_code == 401
        print("Invalid credentials test passed.")

if __name__ == "__main__":
    test_auth()
    print("All tests passed.")
