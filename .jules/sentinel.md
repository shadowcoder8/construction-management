## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2025-02-28 - Hardcoded Secrets in Authentication Fixed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded credentials ("admin" and "admin123") and used standard string comparison which is vulnerable to timing attacks.

**Learning:**
Hardcoded secrets must never be placed in source code as they pose a critical security risk. Environment variables should be used instead. When comparing authentication strings, constant-time comparison methods like `secrets.compare_digest` must be used to mitigate timing attacks.

**Prevention:**
1. Always load sensitive credentials from environment variables or secure vault services.
2. Ensure failure cases (like missing environment variables) are handled securely without leaking information.
3. Use `secrets.compare_digest(string1.encode('utf-8'), string2.encode('utf-8'))` for comparing sensitive strings to prevent timing side channels.
