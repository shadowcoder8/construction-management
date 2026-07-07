## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-05-15 - Consistent Destructive Actions

**Learning:** Destructive actions across the application (like deleting records) lacked consistent UX. While some had confirmation dialogues, others immediately executed deletion which could lead to accidental data loss. Furthermore, visual feedback on success/failure was absent in some functions.

**Action:** Ensured all destructive actions (e.g., `deletePayment`) consistently use native browser `confirm()` dialogues and provide explicit `alert()` success/failure notifications.
