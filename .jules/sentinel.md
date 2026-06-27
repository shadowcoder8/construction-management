## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-11-20 - Hardcoded Credentials in Authentication Fixed

**Vulnerability:**
The `backend/auth.py` application had hardcoded credentials ("admin", "admin123") in the `authenticate_admin` function, posing a critical security risk by exposing login information directly in the source code.

**Learning:**
Authentication logic should never rely on hardcoded secrets, and timing attacks can be prevented during string comparison by using `secrets.compare_digest` with properly encoded byte strings. Furthermore, backend configuration issues (like missing variables) should properly fail out securely (e.g., HTTP 500) rather than failing generically or silently.

**Prevention:**
1. Always use environment variables for sensitive credentials (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`).
2. Utilize secure comparison functions like `secrets.compare_digest` instead of simple string equality (`==`) to mitigate timing attacks.
3. Validate required environment configurations during application startup or execution, throwing specific HTTP 500 errors to inform administrators while hiding stack traces from users.
