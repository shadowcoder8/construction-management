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

## 2025-02-23 - Authorization Bypass on Core API Endpoints

**Vulnerability:**
Multiple core API endpoints (such as `/labours/`, `/attendance/`, `/materials/`, `/sites/`, `/payments/`) and their respective management pages were missing authentication checks. Anyone could access, create, modify, or delete sensitive data without being authenticated.

**Learning:**
Security by obscurity or assuming users will only use the frontend is insufficient. Every sensitive backend route must enforce authorization regardless of the client interface.

**Prevention:**
1. Apply dependency injection (like `Depends(get_current_user)`) consistently on all FastAPI route decorators that handle sensitive data or actions.
2. Develop automated tests to confirm that requests without valid session tokens receive a 401 Unauthorized status.
