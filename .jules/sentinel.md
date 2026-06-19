## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-19 - Hardcoded Admin Credentials in Authentication Logic

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` had hardcoded credentials ("admin", "admin123"). It also used plain string comparison (`==` / `!=`), which is vulnerable to timing attacks.

**Learning:**
Hardcoded credentials are a critical security vulnerability, and plain string comparisons can lead to timing attacks. Additionally, when using `secrets.compare_digest` for secure string comparison, inputs should be encoded (e.g., using `.encode('utf-8')`) to prevent `TypeError` exceptions if the inputs contain non-ASCII characters.

**Prevention:**
1. Do not hardcode credentials in source code. Retrieve them from environment variables (e.g., `os.environ.get("ADMIN_USERNAME")`).
2. Always use `secrets.compare_digest` to verify passwords or tokens to prevent timing attacks.
3. Encode string inputs to `utf-8` bytes before passing them to `secrets.compare_digest` to prevent runtime errors with non-ASCII characters.
