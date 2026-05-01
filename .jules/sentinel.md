## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-01 - [Missing Authentication on Critical Endpoints]
**Vulnerability:** Several critical API endpoints in `main.py` (e.g., `/labours/`, `/attendance/`, `/materials/`, `/sites/`, `/payments/`) lacked the `get_current_user` dependency, exposing sensitive operations without authentication.
**Learning:** The FastAPI application was initially set up with a `get_current_user` dependency to check session cookies, but this dependency was not consistently applied to all API endpoints beyond the dashboard routes.
**Prevention:** Ensure that all endpoints serving sensitive data or performing state-changing operations are protected by incorporating the `current_user: dict = Depends(get_current_user)` parameter in their function signatures, enforcing the application's authentication mechanism universally.
