## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-29 - Hardcoded Admin Credentials and Timing Attack Vulnerability Fixed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded credentials (`"admin"` and `"admin123"`) directly in the source code. Additionally, the string comparison (`username != "admin" or password != "admin123"`) was vulnerable to timing attacks, allowing an attacker to potentially guess the credentials by measuring the time taken for the comparison to fail. The `admin_login` route also caught all exceptions and leaked internal error strings to the client via `str(e)`.

**Learning:**
Credentials must never be hardcoded, as they can be easily extracted by anyone with source code access. Standard string comparisons should be avoided for security-critical checks like passwords or API keys, as they leak timing information. Error handling should be generic for client responses while logging the full details on the server to prevent information disclosure.

**Prevention:**
1. Store sensitive configuration (like usernames and passwords) in environment variables or a secure secret manager.
2. Use `secrets.compare_digest(string1.encode('utf-8'), string2.encode('utf-8'))` for all sensitive string comparisons to ensure constant-time execution and prevent timing attacks.
3. Catch explicit exceptions like `HTTPException` to preserve HTTP status codes (like 500 for missing config), and use a generic `HTTPException(status_code=401, detail="Invalid credentials")` for general failures without exposing internal `str(e)` details.
