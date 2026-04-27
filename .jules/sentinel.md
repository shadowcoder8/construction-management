## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.

## 2024-05-19 - [Hardcoded Credentials & Timing Attacks]
**Vulnerability:** Hardcoded administrative credentials and string comparison vulnerable to timing attacks in `backend/auth.py`.
**Learning:** Hardcoding credentials exposes access to anyone who can read the source code. Regular string comparison (`==` or `!=`) stops at the first mismatched character, allowing attackers to guess passwords character by character by measuring response times.
**Prevention:** Always load credentials from environment variables. Use `secrets.compare_digest()` for comparing sensitive strings like passwords or tokens to ensure comparison time depends only on string length.