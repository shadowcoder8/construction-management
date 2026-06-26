## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-26 - Hardcoded Credentials and Exception Leakage in Authentication

**Vulnerability:**
The `authenticate_admin` function used hardcoded credentials (`"admin"` and `"admin123"`) instead of environment variables. The `admin_login` route in `main.py` leaked internal error details in its `HTTPException` response by returning `str(e)`.

**Learning:**
Authentication logic should never use hardcoded credentials in the source code. Storing and transmitting passwords directly and leaking exceptions to users is a security risk.

**Prevention:**
1. Use environment variables (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`) to provide secrets to the application securely.
2. Use `secrets.compare_digest` with UTF-8 encoding to prevent timing attacks.
3. Catch specific exceptions where necessary, and ensure generic error messages are returned to the user when catching generic `Exception`s, masking stack traces and internal application states.
