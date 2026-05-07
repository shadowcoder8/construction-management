## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.

## 2023-11-20 - Missing Authentication on Sensitive API Endpoints
**Vulnerability:** Several sensitive endpoints (`/materials/`, `/sites/`, `/payments/`, `/attendance/`, and `/labours/`) in `main.py` lacked authentication, allowing unauthorized users to access and potentially manipulate core application data.
**Learning:** The application utilizes a global authentication dependency (`get_current_user`), but it must be manually added to each new protected route. This can easily lead to missed endpoints during active development.
**Prevention:** Establish a systematic approach to secure by default, such as utilizing an APIRouter with a global dependency for all administrative endpoints, or employing static analysis tools and unit testing specifically designed to check authentication enforcement across the API surface.
