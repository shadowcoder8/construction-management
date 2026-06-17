## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-08-01 - Form Accessibility
**Learning:** This application heavily relies on `placeholder` attributes instead of visible `<label>` tags for form inputs across its various HTML files. This causes accessibility issues for screen readers. Adding `aria-label` to these interactive elements (inputs, selects, textareas) is an effective way to fix this without breaking the existing layout.
**Action:** Always add `aria-label` attributes to input, select, and textarea elements to provide screen reader accessibility, since visible `<label>` tags are missing. Note: `aria-label` shouldn't be added to `input[type="hidden"]`.
