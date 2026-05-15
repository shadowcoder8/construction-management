## 2024-05-18 - Non-blocking File I/O with FileResponse

**Pattern:** Replacing synchronous `open().read()` calls with `FileResponse` in async FastAPI routes.

**Learning:** When serving static files or returning file contents in FastAPI, using synchronous `open()` inside an `async def` route blocks the entire event loop, severely degrading performance under load. Since the environment did not have `aiofiles` installed, the most idiomatic and performant solution is to use `fastapi.responses.FileResponse`. `FileResponse` automatically handles setting the correct headers (like `Content-Type` and `Content-Length`) and offloads the file I/O to a thread pool via `anyio`, ensuring the event loop remains responsive.

**Action:** Replaced all instances of `with open(...) as file: return file.read()` with `return FileResponse(...)` across multiple HTML-serving routes (`read_root`, `admin_dashboard`, `labor_management`, `materials_management_page`, `read_payments_management`). This change makes the code more concise, removes blocking calls, and relies on built-in optimal FastAPI features without adding extra dependencies.
