## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Adding Accessibility to Form Placeholder UIs
**Learning:** This app heavily relies on placeholders instead of visible `<label>` tags for form inputs. While this saves space visually, it causes accessibility issues because screen readers may not read the placeholder when focusing the input, and placeholders are often styled with low contrast.
**Action:** Always add `aria-label` attributes to `input`, `select`, and `textarea` elements (ignoring hidden inputs) when standard labels are missing to ensure form context is communicated to assistive technologies.
