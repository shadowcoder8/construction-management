## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2026-05-30 - [Hardcoded Credentials & Timing Attack]
**Vulnerability:** Hardcoded credentials for the admin login in `backend/auth.py` and using a basic string comparison which is vulnerable to timing attacks.
**Learning:** Hardcoded credentials should never be in the codebase, and sensitive string comparisons (like passwords or tokens) must be done in constant time to prevent timing attacks.
**Prevention:** Use environment variables for sensitive configuration and use `secrets.compare_digest` for secure string comparison.
