## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2025-05-18 - [Hardcoded Admin Credentials & Timing Attack Vulnerability]
**Vulnerability:** Admin authentication credentials were hardcoded directly in `backend/auth.py` ("admin" / "admin123") and string comparison was used. This exposed secrets in source code and made it vulnerable to timing attacks during comparison.
**Learning:** Hardcoded credentials are a critical risk, especially for admin accounts. Basic string comparison for passwords leaks timing information which can be exploited to guess the password byte by byte.
**Prevention:** Always retrieve secrets from environment variables (e.g., `ADMIN_USERNAME` and `ADMIN_PASSWORD`) rather than hardcoding them. Use constant-time string comparison functions like `secrets.compare_digest` to mitigate timing attacks.
