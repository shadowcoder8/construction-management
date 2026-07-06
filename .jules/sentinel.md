## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-18 - Hardcoded Admin Credentials Vulnerability

**Vulnerability:**
The `backend/auth.py` file contained hardcoded admin credentials (`username != "admin"` or `password != "admin123"`) directly in the source code. This is a critical security vulnerability that exposes administrative access to anyone who can read the repository. Furthermore, the standard string comparison `!=` is vulnerable to timing attacks.

**Learning:**
Hardcoded credentials are a common but severe risk, especially in initial project templates. Authentication checks should never use simple string comparisons, as it allows attackers to guess valid credentials character-by-character based on response time.

**Prevention:**
1. Always store sensitive credentials (like passwords, API keys, admin usernames) in environment variables or a secure vault, never in source code.
2. Use `secrets.compare_digest(a.encode('utf-8'), b.encode('utf-8'))` for comparing sensitive strings to prevent timing attacks, and always encode to avoid TypeErrors with non-ASCII characters.
3. Fail securely by raising a 500 error if required authentication configuration (like environment variables) is missing, rather than defaulting to an insecure state.
