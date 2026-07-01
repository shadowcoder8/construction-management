## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-07-01 - Hardcoded Admin Credentials Fixed

**Vulnerability:**
The `backend/auth.py` file contained hardcoded credentials (`"admin"` and `"admin123"`) used for authenticating the `admin_login` endpoint. Storing credentials directly in the source code is a critical vulnerability as it exposes them to anyone with read access to the repository, leading to potential unauthorized access and compromise of the system. In addition, string comparison was done using basic equality operators (`==` or `!=`) instead of a constant-time comparison, which can lead to timing attacks. Finally, error messages exposed stack traces or exception details (`str(e)`).

**Learning:**
Authentication secrets and credentials must always be managed securely outside the source code, such as through environment variables or secure secret managers. Time-based attacks on authentication endpoints can be prevented by employing secure comparison functions. Fallback exception handlers should return safe, generic error messages rather than leaking internal details.

**Prevention:**
1. Never hardcode credentials, secrets, or API keys in the source code.
2. Rely on environment variables (e.g., `os.environ.get()`) to inject sensitive data.
3. Use `secrets.compare_digest` (with strings encoded to bytes) to prevent timing attacks.
4. Ensure error messages do not leak internal exception specifics to the client.
