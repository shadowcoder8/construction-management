## 2024-05-18 - [Offload Google Drive API to Threadpool]

**Learning:** The Google Drive API client executes operations synchronously which can severely block an async event loop (like FastAPI). I learned that offloading operations like `execute()` and `next_chunk()` using `asyncio.to_thread` improves concurrency. Specifically, I wrapped things like `service.files().list(...).execute` instead of wrapping the call `execute()`, to pass the method reference. This prevents blocking other handlers handling incoming requests.

**Action:** Added `import asyncio` and wrapped `execute` and `next_chunk` from the googleapiclient calls in `upload_file_to_drive` and `download_file_from_drive` within `backend/utility.py` with `await asyncio.to_thread`.
