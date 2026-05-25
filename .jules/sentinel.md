## 2024-05-24 - [Remove Hardcoded Secrets and Fix Info Leakage]
**Vulnerability:** The `backend/auth.py` file had hardcoded credentials ("admin" and "admin123") used for authentication, presenting a critical security risk. Additionally, the string comparison used for authentication was vulnerable to timing attacks. Finally, the login endpoint in `main.py` leaked error details `str(e)` on failure, posing an information disclosure risk.
**Learning:** Development placeholders and generic try-catch blocks often make it to production without being updated to use secure environment variables and generic user-facing error messages. This codebase lacked validation to ensure sensitive environment variables were properly configured.
**Prevention:**
1. Always use environment variables for sensitive credentials (e.g., `os.getenv`).
2. Use `secrets.compare_digest` for password/credential verification to avoid timing attacks.
3. Catch specific exceptions (like `HTTPException`) and ensure generic `Exception` handlers do not return `str(e)` to the client to avoid information leakage. Ensure 500 errors fail securely.
