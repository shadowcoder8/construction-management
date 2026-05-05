## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Admin Credentials]
**Vulnerability:** Hardcoded administrative credentials ("admin" and "admin123") in `backend/auth.py`.
**Learning:** Hardcoded credentials allow any attacker with source code access to trivially compromise the entire application.
**Prevention:** Store sensitive configuration like default admin passwords in environment variables, and use `secrets.compare_digest` for timing-attack safe comparison.
