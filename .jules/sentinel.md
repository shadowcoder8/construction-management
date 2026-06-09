## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-09 - [Fix Hardcoded Admin Credentials and Error Leakage]
**Vulnerability:** Admin authentication credentials were hardcoded directly in `backend/auth.py`. Additionally, the login endpoint in `main.py` leaked internal error messages (such as missing configuration errors) directly to the client via generic `Exception` blocks.
**Learning:** Hardcoded credentials are a critical risk, especially for admin endpoints. Furthermore, timing attacks can be mitigated by using constant-time string comparisons. Catching bare `Exception` classes without selectively handling expected backend HTTP exceptions risks obscuring the true root cause (e.g., a 500 configuration issue manifesting as a 401 generic error) and exposing server internals.
**Prevention:** Always read sensitive configuration and credentials from the environment (`os.getenv`). When comparing secure strings, employ `secrets.compare_digest` with utf-8 encoding to prevent timing attacks and `TypeError` exceptions. Only catch specific exceptions, re-raise explicitly handled `HTTPException`s, and return sanitized, generic error details for unhandled exceptions to avoid exposing internal logic or stack traces.
