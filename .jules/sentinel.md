## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-20 - Hardcoded Admin Credentials Fixed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded plaintext credentials ("admin" and "admin123") in its source code. This is a critical security risk because anyone with read access to the source code can view the credentials and gain administrative access to the system.

**Learning:**
Never commit sensitive credentials directly in the codebase. When adding authentication logic (even if deemed a "dummy" or placeholder initially), always externalize the credentials using environment variables. Also, when validating user inputs against sensitive data, use constant-time string comparisons (like `secrets.compare_digest`) and remember to encode the strings to bytes (`utf-8`) to prevent `TypeError` exceptions on non-ASCII characters and timing attacks.

**Prevention:**
1. Use environment variables (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`) to store and retrieve credentials in production and development environments.
2. Use Python's `secrets.compare_digest` with `.encode('utf-8')` for secure, constant-time comparison of sensitive string data.
3. Raise a `500 Internal Server Error` if essential authentication configurations are missing in the environment, rather than allowing a fail-open scenario or masked error.
