## 2024-04-25 - [Semantic HTML for Dashboard Cards]
**Learning:** Found an accessibility issue pattern specific to this app where dashboard navigation cards were created using `<div>` tags with `onclick` handlers, relying on JavaScript for navigation. This breaks native keyboard navigation, screen reader support, and standard browser actions (like opening in a new tab). Also, using `alt` text identical to visible text in cards causes redundant screen reader announcements.
**Action:** Always prefer semantic HTML elements (like `<a>` for navigation links) over `<div>`s with JavaScript handlers. For images in links where the link text already describes the destination, use `alt=""` for the image. Ensure interactive elements have distinct focus states using `:focus-visible`.
## 2024-11-20 - [Forms rely on placeholders over labels]
**Learning:** Found an accessibility issue pattern where HTML forms heavily rely on `placeholder` attributes instead of visible `<label>` tags. This lack of proper labeling breaks screen reader support.
**Action:** To ensure accessibility for screen readers without breaking the existing layout, always add `aria-label` attributes to input and select elements.
