## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-08-01 - Hardcoded Admin Credentials Removed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` used hardcoded credentials (`admin` / `admin123`) to authenticate admins. This creates a severe security risk by embedding sensitive secrets directly in the source code, exposing them to anyone with repository access.

**Learning:**
Never hardcode secrets. Always use environment variables for sensitive configuration like passwords and API keys. Additionally, using standard string equality checks (`==`) for passwords enables timing attacks; use `secrets.compare_digest` instead.

**Prevention:**
1. Use `os.environ.get()` to securely retrieve configuration variables.
2. Use `secrets.compare_digest()` after encoding strings to `utf-8` to perform constant-time comparisons.
3. Fail securely (e.g., return a `500 Internal Server Error` if configuration is missing, rather than allowing a default fallback).