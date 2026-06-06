## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2026-06-06 - Hardcoded Secrets Removed

**Vulnerability:**
The `authenticate_admin` function in `backend/auth.py` contained hardcoded admin credentials. Additionally, the string comparison for passwords used standard equality operators rather than constant-time comparison methods, increasing the risk of timing attacks.

**Learning:**
Always use secure environment variables or a configuration manager for sensitive credentials instead of embedding them in the source code. Employ cryptographic string comparison functions like `secrets.compare_digest` to prevent timing attacks. Additionally, remember to encode inputs to byte arrays when comparing strings securely to account for arbitrary character mappings.

**Prevention:**
1. Configure credentials securely using environment variables (`ADMIN_USERNAME` and `ADMIN_PASSWORD`).
2. Utilize `secrets.compare_digest` while comparing potentially sensitive data.
