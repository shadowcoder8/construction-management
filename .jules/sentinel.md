## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-11-20 - Hardcoded Secrets and Timing Attack in Authentication Fixed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded credentials (`"admin"` and `"admin123"`), exposing sensitive info in the codebase. Additionally, the string comparison operator (`!=`) was used for checking credentials, making the authentication vulnerable to timing attacks. Finally, the exception handling in `main.py` for the login route exposed internal error messages by returning `str(e)` in an `HTTPException`.

**Learning:**
Never commit secrets or default credentials into the repository. Authentication should use secure, constant-time comparisons to prevent information leakage through timing attacks. Error handling should avoid leaking sensitive internal details like stack traces or unhandled exception strings.

**Prevention:**
1. Use environment variables (like `ADMIN_USERNAME` and `ADMIN_PASSWORD`) to provide configuration without hardcoding secrets.
2. Use constant-time comparison methods like `secrets.compare_digest()` for password and username checks.
3. Catch unexpected errors and return generic error messages instead of leaking `str(e)` to the client.
