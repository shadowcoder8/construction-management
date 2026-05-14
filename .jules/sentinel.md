## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-14 - Fix Hardcoded Admin Credentials
**Vulnerability:** Admin login was hardcoded as "admin/admin123" directly in `backend/auth.py`, allowing easy source code analysis to gain unauthorized system access. It also used basic string equality checking, making it vulnerable to timing attacks.
**Learning:** Security credentials must never be committed to source code or hardcoded. Comparing strings byte by byte manually can leak information via timing differences.
**Prevention:** Always use environment variables for sensitive data. Use `secrets.compare_digest` when verifying passwords or tokens against expected values to prevent timing attacks. Fail securely with generic HTTP 500 status if configuration variables are missing.
