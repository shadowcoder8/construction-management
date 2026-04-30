## 2024-04-25 - [Semantic HTML for Dashboard Cards]
**Learning:** Found an accessibility issue pattern specific to this app where dashboard navigation cards were created using `<div>` tags with `onclick` handlers, relying on JavaScript for navigation. This breaks native keyboard navigation, screen reader support, and standard browser actions (like opening in a new tab). Also, using `alt` text identical to visible text in cards causes redundant screen reader announcements.
**Action:** Always prefer semantic HTML elements (like `<a>` for navigation links) over `<div>`s with JavaScript handlers. For images in links where the link text already describes the destination, use `alt=""` for the image. Ensure interactive elements have distinct focus states using `:focus-visible`.

## 2024-11-20 - Adding `aria-label` to placeholder-only forms
**Learning:** This app heavily relies on `placeholder` attributes instead of visible `<label>` tags for form layout. This poses an accessibility challenge as screen readers may not read placeholders correctly.
**Action:** When adding inputs or selects, always add `aria-label` attributes to maintain accessibility without breaking the existing UI layout constraints.
