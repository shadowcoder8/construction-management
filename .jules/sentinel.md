## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-24 - Hardcoded Admin Credentials Fixed

**Vulnerability:**
The `backend/auth.py` file contained hardcoded administrative credentials (`"admin"` and `"admin123"`). Additionally, string comparison logic was susceptible to timing attacks.

**Learning:**
Hardcoded credentials are a critical security vulnerability that allow anyone with source code access to bypass authentication. Using environment variables is the proper way to inject credentials at runtime without exposing them. Also, string comparison (`==`) for sensitive data (like passwords) leaks timing information.

**Prevention:**
1. Always read sensitive configuration and credentials from environment variables (e.g., `os.environ.get("ADMIN_PASSWORD")`).
2. Implement safety checks to raise errors (e.g., `500 Internal Server Error`) if the system starts without required configuration.
3. Use `secrets.compare_digest` with UTF-8 encoded strings to mitigate timing attacks and handle potential `TypeError` exceptions related to non-ASCII input handling during secure comparison.
