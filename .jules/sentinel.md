## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Admin Secrets and Timing Attack Risk]
**Vulnerability:** Admin username and password were hardcoded in `backend/auth.py`, and validation used simple string equality (`==`) which is vulnerable to timing attacks. Furthermore, internal error stack traces could leak through the `/admin/login/` endpoint via `str(e)`.
**Learning:** Hardcoding credentials risks source code exposure, while string equality for secret comparison risks timing attacks. Broad exception handling without scrubbing details leaks internal state to attackers. Re-raising `HTTPException` natively prevents masking backend configuration issues (like missing `.env` vars) as generic `401 Unauthorized` responses.
**Prevention:** Use environment variables for sensitive configuration, compare secrets using `secrets.compare_digest()`, and handle errors securely by passing generic responses for unknown errors.
