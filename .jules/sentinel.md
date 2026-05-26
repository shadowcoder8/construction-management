## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.## 2024-05-26 - [Remove Hardcoded Secrets]
**Vulnerability:** The admin username and password were hardcoded directly in the source code within `backend/auth.py`.
**Learning:** Hardcoding credentials exposes sensitive information to anyone with access to the source code repository.
**Prevention:** Rely on environment variables instead (e.g. `ADMIN_USERNAME` and `ADMIN_PASSWORD`), use `secrets.compare_digest` for comparison, and enforce strict error handling when these are misconfigured.
