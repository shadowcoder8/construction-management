## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-18 - Hardcoded Admin Credentials Vulnerability

**Vulnerability:**
The `backend/auth.py` file contained hardcoded administrative credentials (`"admin"` and `"admin123"`) directly in the source code, posing a critical security risk as anyone with access to the codebase would have administrative access. Furthermore, string comparisons were vulnerable to timing attacks.

**Learning:**
Never commit secrets, passwords, or API keys directly into the source code. The authentication logic also failed to handle misconfigurations gracefully, which could lead to unexpected behavior if environment variables were missing.

**Prevention:**
1. Use environment variables (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`) to inject secrets securely into the application at runtime.
2. Ensure that application startup or critical routes fail securely (e.g., returning a 500 error) if required environment variables are absent.
3. Use constant-time string comparison functions like `secrets.compare_digest` (encoded to bytes to prevent TypeErrors) to defend against timing attacks.
