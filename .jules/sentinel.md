## 2024-05-18 - [Insecure Session Management]
**Vulnerability:** Insecure session management using the username as the session ID.
**Learning:** Using predictable session IDs makes the application vulnerable to session hijacking and unauthorized access.
**Prevention:** Generate cryptographically secure session IDs using `secrets.token_hex(32)` and set the `httponly=True` flag on session cookies.
## 2024-05-20 - [Hardcoded Credentials & Timing Attacks]
**Vulnerability:** Admin username and password were hardcoded directly in the source code (`backend/auth.py`), and simple string comparison (`!=`) was used, making it susceptible to timing attacks.
**Learning:** Hardcoding credentials exposes sensitive information if the source code is compromised or accidentally leaked. Additionally, regular string comparison can allow attackers to infer valid strings by measuring response times.
**Prevention:** Store sensitive credentials in environment variables and inject them securely at runtime. When verifying passwords or tokens, always use constant-time comparison functions like `secrets.compare_digest()` to mitigate timing attacks. Fail securely (e.g., HTTP 500) if required configuration is missing.
