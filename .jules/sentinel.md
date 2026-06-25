## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-24 - Hardcoded Admin Credentials Fixed

**Vulnerability:**
The `backend/auth.py` file contained hardcoded administrative credentials (`"admin"` and `"admin123"`). This is a critical vulnerability that allows attackers who gain access to the source code to easily compromise the authentication system.

**Learning:**
Code must not contain sensitive credentials embedded directly. Additionally, string comparisons for authentication logic were susceptible to timing attacks, as regular equality checks evaluate characters sequentially.

**Prevention:**
1. Always load sensitive values (such as credentials, keys, or secrets) from secure environment variables (`os.environ.get(...)`) instead of hardcoding them.
2. Use constant-time comparison methods like `secrets.compare_digest(...)` to protect authentication endpoints from timing attacks, and always make sure both operands are appropriately encoded (e.g., using UTF-8) to prevent encoding-related errors.
3. Fail securely by raising a generic 401 error on login failures, but provide specific 500 status code errors for server-side misconfiguration (like missing env vars) without exposing inner exception details or stack traces to the user.
