## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Credentials & Timing Attacks]
**Vulnerability:** Admin credentials ("admin", "admin123") were hardcoded in `backend/auth.py`, and the authentication check (`username != "admin" or password != "admin123"`) was vulnerable to timing attacks. Furthermore, internal error messages were leaked on authentication failure in `main.py`.
**Learning:** Hardcoding credentials in source code exposes them to anyone with repository access. Standard string comparison (`==` or `!=`) for passwords can be exploited via timing attacks to guess the password. Catching general exceptions and returning their text (`str(e)`) leaks internal implementation details to end users.
**Prevention:**
1. Store credentials securely using environment variables (`os.environ.get()`).
2. Use `secrets.compare_digest()` for comparing passwords to prevent timing attacks.
3. Explicitly catch expected HTTPExceptions and return generic error messages for unhandled exceptions to avoid data leakage.
