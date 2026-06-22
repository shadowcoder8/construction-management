## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-22 - Hardcoded Credentials Removed and Error Leakage Prevented

**Vulnerability:**
The `backend/auth.py` file contained hardcoded administrator credentials (`"admin"` and `"admin123"`). Furthermore, the `admin_login` route in `main.py` blindly caught all runtime exceptions and returned the raw `str(e)` in the HTTP 401 response detail. This meant that unhandled backend errors (like a missing dependency or database crash) could leak sensitive stack traces or internal state strings to an attacker.

**Learning:**
1. Hardcoded credentials bypass standard environment configuration and create an immediate critical vulnerability if the codebase is exposed.
2. A naive `except Exception as e:` that returns `str(e)` violates the principle of "Fail securely," as it inadvertently passes backend implementation details to the client on unexpected errors.
3. String comparisons for authentication must be protected against timing attacks, using secure methods like `secrets.compare_digest`, and must be resilient against encoding type errors (e.g., comparing bytes vs strings when handling non-ASCII characters).

**Prevention:**
1. Source all sensitive credentials and API keys strictly from environment variables (e.g., `os.getenv`).
2. Implement secure timing-attack resistant comparisons (e.g., `secrets.compare_digest(user.encode("utf-8"), env.encode("utf-8"))`).
3. Explicitly catch anticipated exceptions (like `HTTPException`) to pass through intentional status codes (like 500 Server Error if the environment is misconfigured). For generic unhandled exceptions, return a safe, generic message like "Invalid username or password" rather than dynamic error text.
