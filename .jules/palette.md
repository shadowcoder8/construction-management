## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Accessible Form Placeholders
**Learning:** This application heavily relies on `placeholder` attributes instead of visible `<label>` tags for form inputs. While this saves space, it breaks accessibility for screen readers.
**Action:** Added `aria-label` attributes to all non-hidden `<input>` and `<select>` elements across management pages to ensure screen readers can announce the purpose of each field, taking care to exclude `<input type="hidden">` to avoid confusing screen reader users with non-interactive elements.
