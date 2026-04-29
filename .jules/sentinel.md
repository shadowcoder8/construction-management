## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Credentials & Timing Attack]
**Vulnerability:** Admin authentication used hardcoded credentials and standard string comparison, which makes it vulnerable to timing attacks.
**Learning:** Hardcoding credentials exposes sensitive information and regular string comparisons can leak the length or parts of a secret string to attackers.
**Prevention:** Always read credentials from environment variables and use `secrets.compare_digest` for secure string comparison when authenticating.
