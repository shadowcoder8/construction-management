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
The `admin_login` route in `main.py` had a generic `except Exception as e:` block that caught all exceptions and returned the exception's string representation `str(e)` to the client inside a 401 Unauthorized response. If an unexpected internal error occurred (e.g. database failure, missing environment variables leading to a 500 error in `authenticate_admin`), the underlying error details or stack trace fragments could be exposed to potential attackers.

**Learning:**
Generic exception handlers that echo the error message back to the client violate the "fail securely" principle and create an Information Exposure vulnerability. Additionally, catching `Exception` indiscriminately in FastAPI can swallow intended `HTTPException` raises (like a 500 from misconfigured credentials), incorrectly returning them as 401s with leaked details.

**Prevention:**
1. Explicitly catch known HTTPExceptions and re-raise them, or handle them appropriately.
2. Catch general `Exception` separately as a fallback and return generic, non-descriptive error messages to the client (e.g., "Internal server error") while logging the actual `str(e)` server-side.
