## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-10-24 - Accessibility for Form Elements

**Learning:** The forms in this application (`frontend/labor-management.html`) heavily rely on `placeholder` attributes rather than visible `<label>` tags for a cleaner UI. While this is a design choice, it completely breaks accessibility for screen readers since there are no visible labels to associate with inputs. Adding `aria-label` directly to the `input` and `select` elements bridges this gap, allowing the UI to remain visually unchanged while becoming fully accessible.

**Action:** Ensure all inputs and selects across the UI include `aria-label`s, especially in placeholder-only form layouts. Always skip adding `aria-label` to hidden inputs (`<input type="hidden">`) as it can confuse screen readers.
