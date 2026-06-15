## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-08-01 - Destructive Actions Confirmation
**Learning:** Adding a native `confirm()` dialog to destructive actions (e.g., deleting payments) prevents accidental data loss and ensures user intent, significantly improving confidence during data management. Consistent success/failure alerts also align UX across related modules.
**Action:** When implementing or fixing deletion logic in the UI, always enforce a native browser `confirm()` dialogue and provide clear outcome alerts before processing network requests.
