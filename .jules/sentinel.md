## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-24 - [Hardcoded Credentials & Information Leakage]
**Vulnerability:** Admin authentication used hardcoded credentials and exposed raw exception details in HTTP responses.
**Learning:** Hardcoding credentials makes them vulnerable to exposure and brute-forcing. Returning raw `str(e)` in APIs can leak internal implementation details to attackers. Moreover, simple equality comparisons for authentication strings are susceptible to timing attacks.
**Prevention:** Use environment variables for sensitive credentials. Use `secrets.compare_digest` for timing-safe string comparison. Always sanitize exception messages returned to clients and re-raise explicit `HTTPException`s where necessary.
