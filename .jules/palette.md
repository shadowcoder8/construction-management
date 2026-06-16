## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2026-06-16 - Adding Accessible Labels for Placeholder-only Forms

**Learning:** When HTML forms heavily rely on `placeholder` attributes instead of visible `<label>` tags to maintain a clean layout, screen readers may lack sufficient context to identify the inputs correctly.

**Action:** Appended `aria-label` attributes to all non-hidden `<input>` and `<select>` elements in form fields across `labor-management.html`, `inventory-management.html`, and `payment-management.html` to ensure accessibility without altering the existing visual design.
