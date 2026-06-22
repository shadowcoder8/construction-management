## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Adding ARIA Labels to Placeholder-Reliant Forms

**Learning:** The application heavily relies on `placeholder` attributes in input fields and select tags rather than visible `<label>` tags. This approach, while space-saving, is insufficient for screen readers and creates accessibility barriers for non-sighted users.
**Action:** When working on form inputs and selects, consistently inject `aria-label` attributes to ensure they are accessible. Avoid adding `aria-label` to hidden inputs (`<input type="hidden">`) as it can incorrectly expose them to screen readers.
