## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Accessible Form Placeholders

**Learning:** When using forms that rely heavily on `placeholder` attributes instead of visible `<label>` tags to save space, screen readers may lack adequate context. Adding `aria-label` attributes to these visible `input` and `select` elements ensures accessibility without breaking the existing visual layout.

**Action:** Added `aria-label` attributes to all visible form fields across `labor-management.html`, `inventory-management.html`, and `payment-management.html`. Ensured hidden inputs (`type="hidden"`) were excluded to prevent screen readers from incorrectly announcing non-interactive elements.
