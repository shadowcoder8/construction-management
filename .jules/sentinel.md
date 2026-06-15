## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-06-15 - Hardcoded Credentials & Timing Attack Vulnerability

**Vulnerability:**
The `authenticate_admin` logic in `backend/auth.py` contained hardcoded credentials (`"admin"` and `"admin123"`). Furthermore, the string comparison operator (`==`) was used, which is susceptible to timing attacks. Finally, error handling for authentication failures in `main.py` leaked internal error details via stringified exceptions.

**Learning:**
Authentication logic must securely compare credentials and fail opaquely. Python's `secrets.compare_digest` should be used instead of `==` to prevent timing attacks. In an API context, exceptions triggered by missing configurations must be correctly bubbled up as `500` server errors, while user-facing authentication failures must be handled generically to avoid leaking application states or internal failures.

**Prevention:**
1. Avoid hardcoding sensitive credentials in source code. Retrieve them from environment variables or secure credential managers.
2. For secure string comparisons, use `secrets.compare_digest` alongside `.encode('utf-8')` to mitigate TypeErrors with non-ASCII characters and timing attacks.
3. Obscure exception details in authentication catch blocks.
