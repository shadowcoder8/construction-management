## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-13 - Authentication Hardcoded Credentials and Information Disclosure Fixed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` had hardcoded credentials (`"admin"` and `"admin123"`). Additionally, string comparison used standard equality operators which are vulnerable to timing attacks. Finally, when an exception occurred during login in `main.py`, the internal error detail was exposed via `detail=str(e)` to the client, leading to information disclosure.

**Learning:**
1. Hardcoded administrative credentials pose a severe security risk and allow immediate unauthorized access if the source code is compromised.
2. In a FastAPI application, returning raw exception messages directly to the user (e.g., `str(e)`) leaks implementation details that can be useful to an attacker.
3. Authentication processes must use constant-time string comparisons (like `secrets.compare_digest`) combined with utf-8 encoding to prevent timing attacks and avoid TypeErrors with non-ASCII characters.

**Prevention:**
1. Always use environment variables (`ADMIN_USERNAME`, `ADMIN_PASSWORD`) to provide secure credentials. Fail securely (e.g. raise a 500 status code) if these variables are missing from the deployment environment.
2. Catch and re-raise explicit `HTTPException` instances, but for generic `Exception` blocks, log the error internally and return a generic `401 Unauthorized` response to the user with a safe message like "Invalid username or password".
3. Always utilize `secrets.compare_digest(var1.encode('utf-8'), var2.encode('utf-8'))` for comparing sensitive string values like passwords.
