## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2026-07-02 - Destructive Action Protection

**Learning:** Users can accidentally trigger destructive actions (like deleting a payment) causing data loss without explicit confirmation UI. Ensuring all destructive action triggers share a unified confirmation interaction pattern is crucial for user confidence.

**Action:** Appended a native `confirm()` dialog before the API delete request in the `deletePayment` function and paired it with a success/error `alert()` to consistently report the outcome, matching patterns elsewhere in the codebase.
