## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Admin Credentials]
**Vulnerability:** Hardcoded credentials `admin`/`admin123` were present in the authentication logic in `backend/auth.py`.
**Learning:** Hardcoding credentials makes applications vulnerable to simple compromise and leaks sensitive information to anyone with access to the source code.
**Prevention:** Store credentials securely using environment variables (`os.environ.get`), ensure the application fails securely (500 error) if variables are missing, and validate credentials using secure comparison like `secrets.compare_digest()` to prevent timing attacks.
