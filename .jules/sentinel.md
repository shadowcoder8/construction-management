## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Credentials & Timing Attack]
**Vulnerability:** Admin authentication used hardcoded credentials and simple string comparison.
**Learning:** Hardcoded credentials are a critical security risk as they can be easily extracted from source code. Simple string comparison is vulnerable to timing attacks, allowing attackers to guess credentials character by character.
**Prevention:** Use environment variables for credentials with fallbacks. Always use constant-time comparison functions like `secrets.compare_digest` for sensitive string comparisons.
