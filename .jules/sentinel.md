## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-20 - [Hardcoded Admin Credentials]
**Vulnerability:** Hardcoded administrative credentials (`admin`/`admin123`) were present directly in `backend/auth.py`.
**Learning:** Hardcoding credentials exposes sensitive access if the source code is compromised or inadvertently leaked, allowing immediate, full administrative access. Additionally, standard string comparisons were used for passwords, enabling potential timing attacks.
**Prevention:** Always read sensitive configuration and credentials from environment variables (`os.environ.get("...")`). Use `secrets.compare_digest` for validating passwords and tokens to protect against timing side-channel attacks.
