## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-08-05 - Adding ARIA Labels to Form Elements

**Learning:** This app heavily relies on `placeholder` attributes instead of visible `<label>` tags to maintain a cleaner layout. This causes an accessibility issue because screen readers might not announce the inputs correctly without explicit labels.

**Action:** Added `aria-label` attributes to all visible `input` and `select` elements across the forms (e.g., labor details, attendance) to ensure screen readers can provide correct context. Skipped `hidden` inputs since they are not interactive and screen readers should not announce them.
