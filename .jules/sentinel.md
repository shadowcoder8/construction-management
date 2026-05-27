## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2026-05-27 - [Hardcoded Admin Credentials]
**Vulnerability:** Hardcoded username and password in 'backend/auth.py'.
**Learning:** Hardcoded credentials are a critical security risk as they can be easily extracted from the source code.
**Prevention:** Store credentials securely using environment variables and use 'secrets.compare_digest' to prevent timing attacks during validation.
