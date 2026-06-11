## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-11 - Hardcoded Admin Credentials Removed

**Vulnerability:**
The `backend/auth.py` file contained hardcoded administrative credentials (`admin` / `admin123`) directly in the source code. This is a critical security vulnerability as it exposes the keys to the application to anyone with read access to the repository, and makes changing passwords require a code deployment. Additionally, the string comparison was a simple `!=` which is susceptible to timing attacks.

**Learning:**
Authentication logic should never rely on hardcoded secrets within the source code. Environment variables provide a safer mechanism to inject secrets at runtime without checking them into version control.

**Prevention:**
1. Use environment variables (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`) to configure secrets dynamically.
2. Ensure secure string comparison using `secrets.compare_digest` to prevent timing attacks, encoding strings to bytes (`utf-8`) to safely handle all character sets.
3. Fail securely if environment variables are not configured (e.g., by throwing an HTTP 500 server error) to prevent default bypass or obscure failures.
