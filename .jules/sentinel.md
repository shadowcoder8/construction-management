## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Credentials in Auth Module]
**Vulnerability:** Hardcoded admin credentials (`admin`/`admin123`) were present in `backend/auth.py`.
**Learning:** Hardcoding sensitive information such as usernames and passwords directly into the source code is a critical vulnerability because any read access to the code compromises the credentials.
**Prevention:** Store credentials securely using environment variables or a secret management system, and compare them securely using functions like `secrets.compare_digest` to prevent timing attacks. Provide a fallback that fails securely (e.g., throwing a 500 error) if environment variables are unset.
