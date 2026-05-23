## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Admin Credentials]
**Vulnerability:** Admin credentials (username and password) were hardcoded in plain text in `backend/auth.py`.
**Learning:** Hardcoding credentials exposes them to anyone with source code access, violating the principle of least privilege and making credential rotation difficult. The string comparison was also vulnerable to timing attacks.
**Prevention:** Store credentials in environment variables and use `secrets.compare_digest` for constant-time comparison to mitigate timing attacks.
