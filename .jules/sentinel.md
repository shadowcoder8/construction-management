## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-07 - Hardcoded Admin Credentials Fixed

**Vulnerability:**
The `backend/auth.py` application had hardcoded credentials for the admin user (`admin` and `admin123`). In addition, the exception handler in `main.py` was returning internal exception details (`str(e)`) to the user.

**Learning:**
Never hardcode sensitive information like admin credentials in the source code. It should be securely provided through environment variables. Also, the exception handling should not return internal details to the user to prevent information disclosure. Ensure secure comparison using `secrets.compare_digest` with correct encoding.

**Prevention:**
1. Use environment variables (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`) for sensitive credentials.
2. Use `secrets.compare_digest(user_input.encode("utf-8"), correct_secret.encode("utf-8"))` for secure, constant-time comparison to prevent timing attacks.
3. Handle exceptions correctly: return generic error messages for generic errors, and re-raise explicit `HTTPException`s from backend logic.
