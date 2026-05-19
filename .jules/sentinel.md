## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-19 - [Hardcoded Admin Credentials & Timing Attack Vulnerability]
**Vulnerability:** Admin authentication used hardcoded credentials (`"admin"` / `"admin123"`) and standard string comparison (`==`), leading to credential exposure and vulnerability to timing attacks.
**Learning:** Hardcoded credentials make systems inherently insecure if source code is compromised. Standard string comparison allows attackers to infer valid credentials by measuring response times.
**Prevention:** Source credentials from secure environment variables (`ADMIN_USERNAME`, `ADMIN_PASSWORD`) and use `secrets.compare_digest` to perform constant-time string comparison for all secure authentications.
