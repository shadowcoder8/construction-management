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
The `backend/auth.py` file contained hardcoded credentials (`admin` / `admin123`) within the `authenticate_admin` function for dummy authentication logic.

**Learning:**
Hardcoded credentials pose a critical risk because they provide an easy entry point for unauthorized access if the codebase is exposed. Furthermore, string comparisons using `==` for authentication are vulnerable to timing attacks.

**Prevention:**
1. Never commit secrets, API keys, or passwords into the source code repository. Always read sensitive configuration using environment variables (e.g., `os.getenv`).
2. Implement secure comparisons utilizing functions designed to prevent timing attacks, like `secrets.compare_digest()`, and properly encode inputs to prevent TypeErrors on non-ASCII characters.

## 2024-05-20 - Exception Handling Information Leak in Admin Login

**Vulnerability:**
The `main.py` application had a generic exception handler (`except Exception as e`) in the `/admin/login/` route that would catch all errors and re-raise them as an `HTTPException(status_code=401, detail=str(e))`. This incorrectly exposed internal details (like missing config errors raised as 500 `HTTPException`s from the auth module) directly to the client as strings within a 401 response, leaking internal stack details or configuration state.

**Learning:**
When implementing exception handling in route definitions, generic catch-all handlers (`Exception`) should never reflect raw exception strings (`str(e)`) back to the client. This exposes potentially sensitive internal workings. Furthermore, explicitly throwing `HTTPException` in lower-level logic (like `auth.py`) is ineffective if a higher-level route blindly catches it as a generic `Exception` and changes the status code.

**Prevention:**
1. Explicitly catch framework exceptions (like FastAPI's `HTTPException`) and re-raise them to preserve their intended status code and message.
2. Ensure generic `Exception` handlers return a sanitized, generic error message (e.g., "An unexpected error occurred") without exposing internal exception strings.
