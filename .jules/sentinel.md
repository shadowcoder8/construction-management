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

## 2024-05-20 - Missing Authentication on Sensitive Endpoints

**Vulnerability:**
Several core API endpoints and management pages in `main.py` (e.g., `/labours/`, `/attendance/`, `/materials/`, `/sites/`, `/payments/`, `/materials-management/`, `/payment-management/`) were missing authentication checks. This allowed unauthenticated users to access sensitive data and perform CRUD operations, bypassing authorization entirely.

**Learning:**
Authentication dependencies are not automatically applied to all routes in a FastAPI application unless defined globally. Developers must remember to secure each endpoint individually or configure a router-level dependency to prevent unauthorized access to administrative or sensitive functions.

**Prevention:**
1. Enforce authentication on all core API and management endpoints using `dependencies=[Depends(get_current_user)]` in the route decorators.
2. Regularly review route definitions and implement automated security tests to ensure unauthenticated requests to protected endpoints return a 401 Unauthorized status.
