## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Accessible Form Inputs

**Learning:** When using placeholders instead of visible `<label>` tags for form inputs (which is common for simpler or compact UIs), screen readers may fail to announce the field's purpose correctly if `aria-label` attributes are missing. However, these attributes should not be applied to hidden inputs (`<input type="hidden">`), as this can confuse screen readers by presenting interactive elements that are not actually accessible to the user.

**Action:** Added `aria-label` attributes to all visible inputs and select menus across the application's forms to ensure proper accessibility without altering the existing visual layout.
