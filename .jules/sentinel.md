## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.
## 2024-05-20 - Fix Hardcoded Admin Credentials
**Vulnerability:** Admin credentials were hardcoded in `backend/auth.py` (`"admin"` and `"admin123"`), allowing any attacker reading the code to login as an administrator. The application also lacked a mechanism to securely load these from the environment, and a generic exception handler leaked internals if login failed.
**Learning:** Security fixes must be complete: removing hardcoded secrets must be paired with properly throwing and handling configuration errors (like a 500 when missing `ADMIN_USERNAME`).
**Prevention:** Use environment variables for sensitive settings. Always fail securely (return generic `401 Unauthorized` instead of raw exception details) and protect string comparisons with `secrets.compare_digest`.
