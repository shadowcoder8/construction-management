## 2024-05-15 - Offload Synchronous Google API Calls to Threadpool

**Pattern:** Synchronous blocking network calls (such as those from `googleapiclient`'s `.execute()` or chunked file downloads via `MediaIoBaseDownload`) inside an asynchronous event loop can cause significant loop starvation (e.g., blocking 1.5s straight with 0 event loop iterations).

**Action:** Wrap any blocking network I/O or SDK client calls inside an executor to allow other asynchronous processes to continue.

```python
loop = asyncio.get_running_loop()

# For a single blocking call:
request = service.files().list(...)
results = await loop.run_in_executor(None, request.execute)

# For a loop of blocking calls:
def download_sync():
    with open(LOCAL_FILE_PATH, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

await loop.run_in_executor(None, download_sync)
```

**Anti-pattern to avoid:** Don't use `asyncio.get_event_loop()` in modern Python (3.10+); prefer `asyncio.get_running_loop()` when inside an active async context. Avoid letting ad-hoc binary files like `.db` get included in your git changes.
