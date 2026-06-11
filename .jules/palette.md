## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Adding confirmation dialog to delete action

**Learning:** When performing destructive actions, it is essential to ask for user confirmation to prevent accidental data loss. This was missing from `deletePayment` but was present in other areas of the codebase. It significantly improves UX by mitigating user error.

**Action:** Added a `confirm` dialog inside the async `deletePayment` method that checks for user confirmation before sending a DELETE HTTP request.
