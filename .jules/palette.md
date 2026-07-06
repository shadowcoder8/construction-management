## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-10-24 - Accessible Form Inputs

**Learning:** When HTML forms rely heavily on `placeholder` attributes instead of visible `<label>` tags to save space, screen readers cannot properly announce the input purpose. Adding `aria-label` attributes to `<input>` and `<select>` elements significantly improves accessibility. However, applying `aria-label` to hidden inputs (`<input type="hidden">`) is an anti-pattern as it can cause screen readers to incorrectly interpret them as interactive elements.

**Action:** Always add `aria-label` attributes to visible form elements that lack explicit visible labels, deriving the label text from the placeholder or element ID. Skip hidden elements during this process.
