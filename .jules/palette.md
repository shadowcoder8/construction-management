## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-21 - Accessible Form Controls Without Visible Labels

**Learning:** This application heavily utilizes `placeholder` attributes on form inputs instead of explicit `<label>` elements to achieve a compact, modern UI layout. Without explicit labels, screen readers cannot properly announce the purpose of these form controls.
**Action:** Always add descriptive `aria-label` attributes to visible interactive form elements (e.g., `<input>`, `<select>`, `<textarea>`) when visible labels are missing. Ensure that hidden inputs (`type="hidden"`) are excluded from receiving ARIA labels, as adding them can cause screen readers to incorrectly identify them as interactive elements.
