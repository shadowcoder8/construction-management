## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2025-02-14 - Missing Visible Labels in Forms
**Learning:** The forms in this application (Labor, Inventory, and Payment management) heavily rely on `placeholder` attributes instead of visible `<label>` tags. While this creates a specific visual style, it causes accessibility issues as placeholders can disappear or be poorly supported by screen readers.
**Action:** When adding new forms or modifying existing ones, always ensure that visible `input` and `select` elements include an `aria-label` attribute to maintain accessibility without altering the existing visual design pattern. Avoid adding `aria-label` to hidden inputs (`<input type="hidden">`).
