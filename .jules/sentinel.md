## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-18 - Hardcoded Credentials in Authentication

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded `admin` and `admin123` credentials. Furthermore, strings were checked directly with `==`, exposing the application to timing attacks. Finally, any exceptions raised during the login process in `main.py` were caught and returned in their entirety to the user via the HTTP 401 response detail, leaking stack traces and underlying exception strings to unauthenticated clients.

**Learning:**
Authentication must rely on securely-injected environment variables. When comparing secure strings like passwords or keys, a constant-time comparison tool must be used to mitigate timing attacks. Encoding strings before comparing via digest handles multi-byte character constraints properly. Finally, catch blocks in public routes should never leak internal error states.

**Prevention:**
1. Never hardcode credentials in code. Retrieve them from `os.environ`.
2. Always use `secrets.compare_digest(a.encode('utf-8'), b.encode('utf-8'))` for comparing sensitive strings.
3. Catch explicit exceptions like `HTTPException` where expected, but map broad `Exception` catches to generic user-facing errors (e.g. "Invalid login credentials").
