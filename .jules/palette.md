## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-08-02 - Form Accessibility with Placeholders

**Learning:** When HTML forms heavily rely on `placeholder` attributes instead of visible `<label>` tags for styling or space constraints, screen readers fail to accurately describe the purpose of the input.
**Action:** Consistently added `aria-label` attributes to all `<input>`, `<select>`, and `<textarea>` elements across the project to provide screen readers with context without disrupting the existing visual layout.
