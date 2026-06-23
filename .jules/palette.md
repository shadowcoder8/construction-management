## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-05-18 - Missing ARIA Labels on Placeholder-Only Inputs
**Learning:** The application heavily relies on HTML `placeholder` attributes for form inputs instead of explicit `<label>` tags. Since placeholders disappear when users type and are often missed by screen readers, this poses an accessibility barrier for visually impaired users.
**Action:** Always verify if an input relies solely on a placeholder for context. If so, add a descriptive `aria-label` attribute to the `<input>` or `<select>` element to ensure it's accessible without altering the visual design. Do not add it to `<input type="hidden">`.
