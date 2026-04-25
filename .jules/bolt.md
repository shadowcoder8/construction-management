## 2026-04-24 - Added search debounce and optimized search query
**Learning:** Found that a search filter input field was repeatedly calling .toLowerCase() on the searchTerm inside a loop iterating over every table row, and also doing so synchronously on every keystroke.
**Action:** Adding a debounce prevents UI thread blocking, and hoisting the searchTerm.toLowerCase() outside the loop optimizes the operation. Always check loop contents for operations that yield a static result and can be evaluated before the loop.
