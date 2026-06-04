## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.## 2024-05-18 - [Missing Authentication on Sensitive Endpoints]
**Vulnerability:** CRUD API endpoints for managing labors, attendances, materials, sites, and payments were exposed without any authentication checks in FastAPI.
**Learning:** By default, FastAPI routes are unauthenticated unless explicitly protected by a dependency, making it easy to forget access controls on new endpoints.
**Prevention:** Always include `current_user: str = Depends(get_current_user)` as a parameter in sensitive route definitions, ensuring it is appended to the end to avoid default argument syntax errors.
