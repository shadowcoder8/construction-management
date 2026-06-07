## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2026-06-07 - Add Confirmation Dialog for Destructive Actions

**Learning:** Across the application, some destructive actions like deleting payments did not have confirmation prompts, unlike other entities such as laborers or materials. This lack of consistency and safeguard can easily lead to accidental data loss. A uniform application of `confirm()` dialogues for all destructive actions dramatically improves the UX and prevents accidental deletions.
**Action:** Added a native browser `confirm()` prompt inside `deletePayment` in `payment-management.js`. Going forward, ensure all destructive actions across all modules trigger a confirmation dialogue before calling APIs to modify data.
