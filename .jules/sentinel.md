## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Admin Credentials]
**Vulnerability:** Hardcoded administrative credentials ("admin" / "admin123") in backend authentication logic.
**Learning:** Hardcoded credentials are a critical security risk as anyone with source code access can compromise the application, and they prevent easily rotating secrets. Furthermore, standard string comparison for passwords is theoretically vulnerable to timing attacks.
**Prevention:** Use environment variables (e.g. `ADMIN_USERNAME`, `ADMIN_PASSWORD`) to inject secrets at runtime. Use constant-time comparison methods like `secrets.compare_digest()` to validate credentials to prevent timing-based side-channel attacks.
