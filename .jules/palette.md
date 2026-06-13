## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-05-18 - Missing destructive action confirm dialog in Payment Management
**Learning:** The payment management UI triggers a `DELETE` API call instantly on button click, which goes against existing project patterns and could cause accidental data loss. This was found because I had previously seen similar issues in other sections.
**Action:** Always add native browser `confirm()` dialogs to actions that perform irreversible operations to maintain consistency and prevent user errors.
