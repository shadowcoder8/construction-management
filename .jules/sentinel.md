## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-24 - Hardcoded Admin Credentials Vulnerability
**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded credentials (`"admin"` and `"admin123"`) to validate admin logins. This represents a critical security risk because anyone with access to the source code can find the credentials, and the secret cannot be rotated without changing the codebase. Additionally, basic string comparisons for passwords were used, which are susceptible to timing attacks.

**Learning:**
Authentication secrets should never be hardcoded into the codebase. Secure credential management relies on environment variables, enabling different credentials per environment and secure rotation. Furthermore, credential validation should always employ constant-time comparison methods (like `secrets.compare_digest`) to prevent timing attacks where attackers can guess passwords character by character. Exception handlers on authentication routes should be careful not to leak internal server state (like missing configuration) via general catch-all blocks.

**Prevention:**
1. Always use environment variables (e.g., `os.getenv("ADMIN_USERNAME")`) to manage sensitive configurations and credentials.
2. Use `secrets.compare_digest(a.encode('utf-8'), b.encode('utf-8'))` for any secure string comparison.
3. Ensure missing security configurations (like absent environment variables) result in a fail-secure state, explicitly throwing a 500 error instead of defaulting or bypassing checks.
4. Catch explicit exceptions (like `HTTPException`) first to ensure intentional server responses aren't masked by generic `Exception` blocks that return 401s or expose `str(e)`.
