## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-23 - Hardcoded Authentication Secrets and Error Leakage Fixed

**Vulnerability:**
The `backend/auth.py` file contained hardcoded credentials (`"admin"` and `"admin123"`) instead of relying on environment variables. Additionally, the exception handler for `admin_login` in `main.py` returned the internal exception message (`str(e)`) to clients instead of a generic message.

**Learning:**
Hardcoded secrets make the application immediately vulnerable when the source code is read. Moreover, when building an overarching `except Exception as e` handler, exposing `str(e)` directly inside a 401 response risks leaking framework specifics, variable details, or other context information that shouldn't reach unauthorized users.

**Prevention:**
1. Configure secrets strictly via environment variables (e.g., `os.environ.get("ADMIN_USERNAME")`).
2. Implement secure timing-safe comparisons (e.g., `secrets.compare_digest`).
3. Re-raise specific HTTPExceptions explicitly, and always replace unstructured exceptions with generic failure strings.
