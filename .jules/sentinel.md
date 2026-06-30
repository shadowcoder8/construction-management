## 2024-05-18 - Overly Permissive CORS Configuration Fixed

**Vulnerability:**
The `main.py` application was explicitly configured with `allow_origins=["*"]` within the `CORSMiddleware`. Since authentication might be enabled with cookies, this creates a major risk of Cross-Site Request Forgery (CSRF). While `allow_credentials=True` used with `["*"]` is often restricted by FastAPI or modern browsers, a wildcard origin config on an authenticated backend is fundamentally insecure.

**Learning:**
Always use an environment variable (like `ALLOWED_ORIGINS`) to strictly define and manage authorized clients, falling back to a safe local list during development (`http://localhost:8000,http://127.0.0.1:8000`).

**Prevention:**
1. Do not use wildcard `["*"]` for CORS in production setups, especially with authenticated routes.
2. Verify CORS setups using testing frameworks like Pytest or by configuring restricted inputs dynamically through the `.env` configuration.

## 2024-05-18 - Hardcoded Service Account Credentials in Repository

**Vulnerability:**
The repository contained a `credentials.json` file which was tracked by git. This file held the private key and other sensitive details for a Google Service Account used for Google Drive API synchronization. Committing such files exposes the entire service account and connected cloud resources to anyone with read access to the repository or its history.

**Learning:**
Never commit service account JSON keys or any sensitive credentials directly into the repository. Even if a repository is private, credentials should be managed securely outside of version control. The presence of the file indicated a significant security risk.

**Prevention:**
1. Explicitly add sensitive files (e.g., `credentials.json`, `.env`) to `.gitignore` immediately upon creation.
2. Rely on environment variables (like `GOOGLE_CREDENTIALS_PATH` which was already present in `utility.py`) to specify the path to these files, which should be injected or mounted securely in production environments.
3. Remove accidentally committed secrets from git history if they are compromised, or immediately rotate the keys.
