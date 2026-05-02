## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Admin Credentials]
**Vulnerability:** Hardcoded admin credentials `admin`/`admin123` were present in the authentication logic. Furthermore, string comparison was prone to timing attacks.
**Learning:** Hardcoding credentials makes them trivial to extract, and regular string comparison logic can leak length and character information.
**Prevention:** Store secrets in environment variables instead of hardcoding them, and use `secrets.compare_digest` to perform constant-time comparison.
