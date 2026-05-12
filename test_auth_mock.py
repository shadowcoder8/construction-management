import sys
import os

# Mock the modules
class MockFastAPI:
    class HTTPException(Exception):
        def __init__(self, status_code, detail):
            self.status_code = status_code
            self.detail = detail

sys.modules['fastapi'] = MockFastAPI

from backend.auth import authenticate_admin

def run_tests():
    print("Running tests...")

    # Test 1: Missing env variables
    os.environ.pop("ADMIN_USERNAME", None)
    os.environ.pop("ADMIN_PASSWORD", None)
    try:
        authenticate_admin("admin", "admin123")
        print("FAIL: Expected exception for missing env vars")
        return False
    except MockFastAPI.HTTPException as e:
        if e.status_code == 500:
            print("PASS: Missing env vars -> 500")
        else:
            print(f"FAIL: Missing env vars -> unexpected status code {e.status_code}")
            return False

    # Test 2: Invalid credentials
    os.environ["ADMIN_USERNAME"] = "secureadmin"
    os.environ["ADMIN_PASSWORD"] = "securepass"
    try:
        authenticate_admin("admin", "admin123")
        print("FAIL: Expected exception for invalid credentials")
        return False
    except MockFastAPI.HTTPException as e:
        if e.status_code == 401:
            print("PASS: Invalid credentials -> 401")
        else:
            print(f"FAIL: Invalid credentials -> unexpected status code {e.status_code}")
            return False

    # Test 3: Valid credentials
    try:
        res = authenticate_admin("secureadmin", "securepass")
        if res.get("message") == "Login successful":
            print("PASS: Valid credentials -> success")
        else:
            print("FAIL: Valid credentials -> unexpected response")
            return False
    except Exception as e:
        print(f"FAIL: Valid credentials -> unexpected exception {e}")
        return False

    print("ALL TESTS PASSED")
    return True

if __name__ == "__main__":
    if not run_tests():
        sys.exit(1)
