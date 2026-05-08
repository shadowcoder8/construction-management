## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.

## 2024-05-24 - [Hardcoded Admin Credentials & Insecure Comparison]
**Vulnerability:** Admin credentials ("admin" / "admin123") were hardcoded in `backend/auth.py`, and standard string comparison `!=` was used.
**Learning:** Hardcoded credentials can easily be extracted from the source code. Using standard string comparison for passwords enables timing attacks. Missing env var defaults risk unauthorized access or exposing misconfigurations.
**Prevention:** Use environment variables (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`) to securely inject credentials, use `secrets.compare_digest` for timing-attack safe comparison, and always "fail securely" by raising a 500 error if critical environment variables are missing.