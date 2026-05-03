## 2024-05-03 - [Missing dependency on sensitive API endpoints]
**Vulnerability:** Missing authentication on sensitive endpoints (materials, sites, payments, labors). Anyone could hit the API directly.
**Learning:** Adding the dependency to an endpoint protects it without altering the underlying logic. FastAPI parameters must have default arguments if previous parameters have default arguments to prevent SyntaxError.
**Prevention:** Apply `current_user: dict = Depends(get_current_user)` as a dependency parameter correctly on all API routes modifying or viewing sensitive data.

## 2024-05-03 - [Hardcoded Admin Credentials]
**Vulnerability:** Admin credentials were hardcoded directly in `backend/auth.py`. Furthermore, string equality check was used to verify username and password which made it susceptible to timing attacks.
**Learning:** Using `secrets.compare_digest` is a better practice since it executes in constant time compared to string equality operations.
**Prevention:** Never hardcode credentials and use `os.environ` to access securely. Ensure `secrets.compare_digest` is used for constant-time comparisons when validating passwords and usernames.
