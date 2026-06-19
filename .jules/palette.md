## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Placeholder-Reliant Forms

**Learning:** The application heavily relies on `placeholder` attributes instead of visible `<label>` tags for form inputs. This makes forms largely inaccessible to screen readers, as the purpose of the input isn't explicitly announced.

**Action:** Whenever introducing new inputs or modifying existing forms that rely purely on placeholders, always add explicit `aria-label` attributes to all non-hidden `<input>`, `<select>`, and `<textarea>` elements to ensure screen-reader accessibility without breaking the established visual layout.
