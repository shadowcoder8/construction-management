## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.
## 2024-11-20 - [Hardcoded Admin Credentials]
**Vulnerability:** Found hardcoded credentials `admin` / `admin123` in `backend/auth.py`'s `authenticate_admin` function.
**Learning:** Hardcoding credentials inside code allows any source-code reader to compromise the system. It should be securely checked against environment variables instead.
**Prevention:** Use `os.getenv` to read credentials. Use `secrets.compare_digest` with utf-8 encoding for timing-attack-resistant comparisons. If credentials aren't configured, fail securely by returning a 500 error rather than masking the configuration gap.
