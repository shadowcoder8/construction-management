## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2026-06-05 - [Hardcoded Credentials]
**Vulnerability:** Admin credentials were hardcoded in `backend/auth.py`.
**Learning:** Hardcoding secrets makes them easily accessible to anyone with code access and complicates key rotation. Additionally, string comparison can be vulnerable to timing attacks.
**Prevention:** Use environment variables for sensitive configuration (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`) and use `secrets.compare_digest` with utf-8 encoding for secure string comparison to prevent timing attacks.
