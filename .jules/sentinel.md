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
The `backend/auth.py` file contained hardcoded admin credentials (`username == "admin"` and `password == "admin123"`). This is a critical security vulnerability as it allows anyone with access to the source code to authenticate as an admin.

**Learning:**
Never hardcode credentials or secrets in source code. Use environment variables or secure secret management systems instead.

**Prevention:**
1. Read sensitive configuration values like admin credentials from environment variables (`os.getenv`).
2. Use secure comparison functions like `secrets.compare_digest` to prevent timing attacks when comparing strings.
