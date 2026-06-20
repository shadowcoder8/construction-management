## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-08-01 - Consistent Form Accessibility
**Learning:** The application heavily utilizes `placeholder` attributes instead of visible `<label>` tags for form inputs across its various static HTML files. While clean visually, this practice negatively impacts screen reader accessibility.
**Action:** Consistently added `aria-label` attributes to visible interactive form fields (e.g., `<input>`, `<select>`, `<textarea>`) where explicit labels are missing to ensure compliance, intentionally skipping `<input type="hidden">` to avoid screen reader clutter.
