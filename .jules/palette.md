## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Accessible Form Inputs without Visible Labels

**Learning:** This codebase frequently relies on `placeholder` attributes instead of visible `<label>` tags for form inputs (like laborer details or search bars), which reduces accessibility for screen readers.

**Action:** Consistently added `aria-label` attributes to `input` and `select` elements lacking explicit visible labels, skipping hidden inputs (`type="hidden"`) to prevent confusing screen readers. This improves accessibility without requiring layout changes.
