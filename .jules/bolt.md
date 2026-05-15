## 2026-04-24 - Added search debounce and optimized search query
**Learning:** Found that a search filter input field was repeatedly calling .toLowerCase() on the searchTerm inside a loop iterating over every table row, and also doing so synchronously on every keystroke.
**Action:** Adding a debounce prevents UI thread blocking, and hoisting the searchTerm.toLowerCase() outside the loop optimizes the operation. Always check loop contents for operations that yield a static result and can be evaluated before the loop.
## 2026-05-15 - Offloading synchronous Google API requests in async contexts
**Learning:**
The Google Drive API client (from `googleapiclient`) is fundamentally synchronous. When its methods like `.execute()` or chunked file downloads (`.next_chunk()`) are used inside asynchronous FastAPI endpoints or lifecycle events without proper handling, they block the async event loop. This leads to severe performance degradation as concurrent tasks are forced to wait.
**Action:**
To fix this, we wrapped all synchronous network and file I/O operations provided by the Google API client in `await asyncio.to_thread(...)`. This correctly delegates the blocking tasks to a thread pool, allowing the async event loop to remain responsive and process tasks concurrently.
