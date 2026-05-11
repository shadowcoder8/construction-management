## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Admin Credentials]
**Vulnerability:** Hardcoded administrative credentials ("admin"/"admin123") in `backend/auth.py`.
**Learning:** Hardcoded credentials are a critical security risk as they allow unauthorized access if the codebase is exposed or shared. They cannot be easily rotated without modifying and redeploying the code.
**Prevention:** Use environment variables (e.g., `ADMIN_USERNAME` and `ADMIN_PASSWORD`) to provide credentials dynamically. In Python, retrieve these via `os.environ.get()` and ensure they are present at startup or raise a 500 error. Always use `secrets.compare_digest` for string comparison of sensitive data to prevent timing attacks.
