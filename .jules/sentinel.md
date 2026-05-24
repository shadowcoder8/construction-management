## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-24 - [Hardcoded Credentials & Error Leakage]
**Vulnerability:** Admin authentication used hardcoded credentials (`"admin"`, `"admin123"`) in `backend/auth.py`, making it trivially accessible. Also, `main.py` leaked internal error string details upon login failures.
**Learning:** Hardcoding secrets exposes the application to immediate compromise. In addition, returning unhandled exception string representations to the client leaks implementation details. Using `secrets.compare_digest` is necessary when verifying secrets to prevent timing attacks.
**Prevention:** Use environment variables (via `os.getenv`) to inject sensitive data. Re-raise known API errors (like 500 configuration errors) and use generic messages for unhandled internal exceptions. Employ constant-time string comparisons.
