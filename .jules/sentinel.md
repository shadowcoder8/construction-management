## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-18 - Hardcoded Admin Credentials Vulnerability Fixed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` used hardcoded credentials (`"admin"`/`"admin123"`) and simple string comparison. This poses critical security risks: hardcoded secrets in the source code can be leaked easily, and standard string comparisons are vulnerable to timing attacks. Also, the `admin_login` route in `main.py` had overly generic error handling that masked internal server configuration issues (e.g., missing credentials) by converting all exceptions, including 500 errors, into 401 Unauthorized responses containing the raw error string.

**Learning:**
Authentication logic should never rely on hardcoded credentials. It must read secrets from secure sources like environment variables. When comparing secrets (like passwords or tokens), it's crucial to use timing-safe comparison functions, such as `secrets.compare_digest`, and appropriately handle string encodings to avoid `TypeError`s on non-ASCII input. Furthermore, `HTTPException`s thrown by inner services should be caught and re-raised directly in routers to maintain correct HTTP semantics, rather than being swallowed by generic exception handlers that obfuscate configuration issues or leak unexpected exception details.

**Prevention:**
1. Configure credentials via environment variables (`ADMIN_USERNAME`, `ADMIN_PASSWORD`).
2. Always use `secrets.compare_digest` for secure string comparison of passwords or tokens.
3. Catch explicit `HTTPException`s to re-raise them properly in route handlers before a generic `Exception` catch block.
