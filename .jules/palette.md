## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-08-01 - Adding ARIA labels to placeholder-only inputs

**Learning:** The app's HTML forms heavily rely on `placeholder` attributes instead of visible `<label>` tags to save space. While visually clear, this causes accessibility issues for screen readers. Adding `aria-label` attributes to these input, select, and textarea elements provides the necessary context without altering the visual design.

**Action:** Added `aria-label` attributes to all inputs, selects, and search bars in `frontend/labor-management.html`, `frontend/inventory-management.html`, and `frontend/payment-management.html`.
