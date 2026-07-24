## 2024-08-01 - Modernizing UI

**Learning:** When unifying basic UI across multiple static HTML and CSS files, adding a central set of CSS variables (`:root`) alongside a modern grid framework significantly improves consistency and maintainability. Playwright provides a reliable mechanism to ensure the static DOM files are syntax-error-free and structure looks correct via screenshots during headless local test runs.

**Action:** Rebuilt the frontend CSS and modified static files to inject modern typography (`Inter`), variables for colors, spacing, radius, and standard input/button styling. Verified all `file://` URLs headless using `playwright`.

## 2024-11-20 - Adding Accessibility Labels to Placeholder-Reliant Forms

**Learning:** The application's HTML forms heavily rely on `placeholder` attributes instead of visible `<label>` tags. To ensure accessibility for screen readers without breaking the existing layout or visual design, it is critical to add explicit `aria-label` attributes to all non-hidden input, select, and textarea elements.

**Action:** Added `aria-label` attributes corresponding to the placeholder or intended function for all `input` (excluding `type="hidden"`) and `select` elements across the main management forms (`labor-management.html`, `inventory-management.html`, and `payment-management.html`).

## 2024-07-24 - Dynamic ARIA Labels for Stateful Icon-Only Buttons

**Learning:** When using stateful icon-only buttons (like a password visibility toggle), relying solely on visual icon changes leaves screen reader users unaware of the state change. The `aria-label` must be dynamically updated via JavaScript (e.g., "Show password" to "Hide password") to ensure the accessibility tree remains accurate.

**Action:** Added a password visibility toggle to the login form and included JavaScript logic to dynamically update both the FontAwesome icon and the `aria-label` attribute on click, ensuring an accessible experience for screen reader users.
