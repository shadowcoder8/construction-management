## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2026-04-30 - [Hardcoded Admin Credentials & Timing Attack Vulnerability]
**Vulnerability:** Admin authentication used hardcoded strings ("admin" / "admin123") and basic string equality (`!=`), exposing secrets in source code and risking timing attacks.
**Learning:** Hardcoded credentials should never exist in the codebase. Standard string comparison returns early on a mismatch, allowing attackers to guess credentials byte-by-byte via timing differences.
**Prevention:** Store credentials in environment variables (e.g. `ADMIN_USERNAME`, `ADMIN_PASSWORD`), fail securely (500 error) if they are missing, and always use `secrets.compare_digest` for constant-time comparison.
