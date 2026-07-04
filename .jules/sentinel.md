## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-19 - Hardcoded Admin Credentials in Source Code
**Vulnerability:** The application contained hardcoded administrative credentials (`"admin"` and `"admin123"`) directly in `backend/auth.py` and returned internal exception details in `main.py`'s login route. This allows an attacker who gains access to the source code to easily authenticate as an admin, and the unhandled exceptions could leak sensitive system context.
**Learning:** Hardcoding credentials makes them trivial to extract, and using string comparison for passwords exposes the app to timing attacks. Leaking raw `Exception` details through API error messages can expose backend configuration details to users.
**Prevention:**
1. Always use environment variables (e.g., `os.environ.get("ADMIN_USERNAME")`) to manage sensitive credentials securely outside of version control.
2. Use `secrets.compare_digest` (with `.encode('utf-8')` for string compatibility) for secure string comparison to mitigate timing attacks.
3. Catch and handle exceptions properly in routes, ensuring generic errors like "Unauthorized" are returned for general faults rather than internal stack traces or exact reasons.
