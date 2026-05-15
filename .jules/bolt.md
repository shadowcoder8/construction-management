## 2026-04-24 - Added search debounce and optimized search query
**Learning:** Found that a search filter input field was repeatedly calling .toLowerCase() on the searchTerm inside a loop iterating over every table row, and also doing so synchronously on every keystroke.
**Action:** Adding a debounce prevents UI thread blocking, and hoisting the searchTerm.toLowerCase() outside the loop optimizes the operation. Always check loop contents for operations that yield a static result and can be evaluated before the loop.

## 2026-05-15 - Used standard Python logging over print statements
**Learning:** Found print statements being used for logging errors in exception handlers, which are hard to track in production environments and lack context like timestamps or log levels.
**Action:** Replaced `print` with Python's standard `logging.error` using a module-level logger. Ensure all backend modules initialize their logger (`logger = logging.getLogger(__name__)`) and use standard logging levels.
