## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Adding Form Accessibility

**Learning:** This app heavily relies on `placeholder` attributes instead of visible `<label>` tags for forms. While visually clean, this causes accessibility issues for screen readers.

**Action:** Consistently added `aria-label` attributes to `input`, `select`, and `textarea` elements (excluding hidden inputs) across forms to maintain the existing layout while ensuring proper screen reader support.
