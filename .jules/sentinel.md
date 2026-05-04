## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-04 - [CRITICAL] Fix Hardcoded Admin Credentials in Authentication Logic
**Vulnerability:** Found hardcoded admin credentials (`"admin"`, `"admin123"`) directly in `backend/auth.py`. Also, string equality was used instead of secure comparisons.
**Learning:** Hardcoded secrets in version-controlled source code is a major security flaw allowing immediate unauthorized access. String equality opens up timing attack vectors.
**Prevention:** Store credentials in environment variables (`ADMIN_USERNAME`, `ADMIN_PASSWORD`), read them in at runtime, fail securely if unconfigured, and use `secrets.compare_digest` for timing-attack resistance.
