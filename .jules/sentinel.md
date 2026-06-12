## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.
## 2025-02-14 - Replace Hardcoded Credentials with Environment Variables
**Vulnerability:** The `authenticate_admin` function in `backend/auth.py` contained hardcoded credentials (`"admin"` / `"admin123"`) compared using standard `==` operators.
**Learning:** Hardcoding credentials exposes sensitive information and facilitates unauthorized access. Furthermore, standard string comparisons (`==`) can be susceptible to timing attacks, allowing malicious actors to infer credentials by measuring the time it takes the server to reject different guesses.
**Prevention:** Always externalize secrets into environment variables (e.g., `ADMIN_USERNAME`, `ADMIN_PASSWORD`). Fail securely by raising a 500 error if these variables are missing to prevent unexpected behavior. Use `secrets.compare_digest` with utf-8 encoding for secure, constant-time string comparisons to prevent timing attacks.
