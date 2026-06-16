## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-16 - Hardcoded Credentials & Authentication Timing Attack Fixed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded credentials ("admin", "admin123") and used standard string comparison `==`, which is susceptible to timing attacks. Furthermore, errors during login logged full exception details natively, which could result in potential information disclosure if generic exceptions leaked internal details or state to an attacker.

**Learning:**
Authentication logic should never rely on hardcoded secrets, and timing attacks must be mitigated by using constant-time comparison methods, such as `secrets.compare_digest`. Exception handling on unauthenticated routes must fail securely, returning generic responses like "Invalid username or password" rather than leaking internal strings.

**Prevention:**
1. Configure secrets via environment variables (`ADMIN_USERNAME`, `ADMIN_PASSWORD`) and validate their presence.
2. Use `secrets.compare_digest` (with strings encoded to `utf-8`) for secure credential matching.
3. Catch generic `Exception`s and raise explicitly generic `HTTPException` responses (like 401 Unauthorized with standard phrasing) to avoid disclosing system context.
