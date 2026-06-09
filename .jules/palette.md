## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-08-01 - Accessible Placeholder Forms

**Learning:** When HTML forms heavily rely on `placeholder` attributes instead of visible `<label>` tags for styling reasons, screen readers may not reliably announce the field's purpose. However, applying `aria-label` attributes globally is dangerous: adding them to hidden inputs (`<input type="hidden">`) can cause screen readers to incorrectly interpret them as interactive elements.

**Action:** Consistently added `aria-label` attributes to visible `input`, `select`, and `textarea` elements that lack explicit labels, while ensuring they are explicitly excluded from `type="hidden"` elements to maintain proper screen reader flow.
