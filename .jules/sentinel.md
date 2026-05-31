## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.

## 2024-05-31 - [Hardcoded Admin Credentials & Exception Leak]
**Vulnerability:** Admin authentication used hardcoded string values ("admin", "admin123") in `backend/auth.py`, and the `admin_login` route in `main.py` leaked Python exception messages (`str(e)`) to the client when a 401 Unauthorized was returned.
**Learning:** Hardcoded credentials in source code pose a critical security risk as they can be easily extracted from the repository or compiled assets. Leaking stack trace or internal exception strings exposes system details that can be used for further attacks.
**Prevention:** Always load secrets from environment variables and use constant-time comparison methods like `secrets.compare_digest` for authentication. Catch specific HTTP exceptions to manage logic correctly, and fall back to generic user-facing messages ("Unauthorized") for unexpected errors.
