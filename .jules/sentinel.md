## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-18 - Hardcoded Admin Credentials in Authentication Logic Fixed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded, easily guessable credentials (`admin` / `admin123`) compared using standard string equality. This is a critical risk, allowing trivial unauthorized access to administrative functions, and the use of standard equality opens up potential timing attacks for credential discovery.

**Learning:**
Code containing dummy or placeholder logic for authentication is frequently pushed to production. Always verify that authentication mechanisms validate against securely stored or injected credentials (like environment variables or databases).

**Prevention:**
1. Never hardcode sensitive credentials (passwords, API keys) in the source code.
2. Use environment variables (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`) to configure credentials for the environment.
3. Use a constant-time comparison function, such as Python's `secrets.compare_digest()`, when comparing passwords or tokens to prevent timing attacks. Always encode the strings to UTF-8 before comparison to handle any non-ASCII characters without raising TypeErrors.
4. Fail securely (e.g., return HTTP 500) if required security configurations are missing.
