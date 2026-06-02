## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-15 - Hardcoded Credentials in Authentication Endpoint
**Vulnerability:** Hardcoded admin credentials ("admin"/"admin123") were found in `backend/auth.py`. Hardcoded credentials can easily be extracted from the codebase and used to compromise the system. The string comparison was also using standard `!=` operator, making it vulnerable to timing attacks.
**Learning:** Development placeholders for authentication are often left in production if not explicitly tracked. Simple string comparison operators short-circuit, allowing attackers to guess passwords character by character based on response time.
**Prevention:** Use environment variables (e.g., `os.environ.get`) for all secrets. Always use `secrets.compare_digest` for cryptographic string comparisons to defend against timing attacks. Ensure the application fails securely (e.g., 500 error) if secrets are unconfigured.
