## 2024-05-24 - Async Lifespan Blocking
**Anti-pattern:** Using synchronous network/file I/O in FastAPI `lifespan` blocks or async routes without `asyncio.to_thread`.
**Learning:** Google Drive API `build` and `.execute()` calls are synchronous. Running them directly in FastAPI's async context blocks the event loop and can cause startup crashes or `TypeError: expected str, bytes or os.PathLike object, not NoneType` when credentials fail.
**Action:** Wrapped Drive API `.execute()` and `.next_chunk()` calls with `await asyncio.to_thread()` and added graceful degradation in `authenticate_google_drive` and `main.py`'s lifespan to skip sync if credentials are missing or invalid, preventing app crashes on Render.
