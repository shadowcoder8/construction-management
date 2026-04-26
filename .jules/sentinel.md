## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-18 - [Hardcoded Credentials & Leaked Secrets]
**Vulnerability:** Hardcoded admin credentials (`admin`/`admin123`) in `backend/auth.py` and a committed Google Service Account private key in `credentials.json`.
**Learning:** Hardcoding credentials and committing sensitive files (like service account keys) exposes the application to immediate unauthorized access and privilege escalation.
**Prevention:** Always use environment variables for sensitive configuration (`os.getenv`). Use `secrets.compare_digest` to prevent timing attacks during authentication. Ensure `.gitignore` includes sensitive files (e.g., `*.json` containing secrets).
