## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Adding Accessibility Labels

**Learning:** When inputs and selects rely entirely on placeholder text without explicit `<label>` tags, screen readers can struggle to provide enough context for the users. Adding `aria-label` directly to these form controls fills that accessibility gap quickly without breaking the existing UI layout.

**Action:** Added `aria-label` properties to all relevant text inputs and select inputs on the Labor, Inventory, and Payment management HTML forms. Verified using a python script with `html.parser.HTMLParser` testing for the `aria-label` presence.
