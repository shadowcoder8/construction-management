## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.## 2024-05-16 - Hardcoded Secrets in Authentication
**Vulnerability:** Admin credentials were hardcoded in `backend/auth.py`, posing a critical security risk.
**Learning:** Hardcoded credentials can easily be extracted from the source code.
**Prevention:** Read secrets from environment variables (e.g., `os.environ.get`) and use constant-time string comparisons (e.g., `secrets.compare_digest`) to prevent timing attacks.
