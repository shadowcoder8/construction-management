## 2024-04-25 - [Semantic HTML for Dashboard Cards]
**Learning:** Found an accessibility issue pattern specific to this app where dashboard navigation cards were created using `<div>` tags with `onclick` handlers, relying on JavaScript for navigation. This breaks native keyboard navigation, screen reader support, and standard browser actions (like opening in a new tab). Also, using `alt` text identical to visible text in cards causes redundant screen reader announcements.
**Action:** Always prefer semantic HTML elements (like `<a>` for navigation links) over `<div>`s with JavaScript handlers. For images in links where the link text already describes the destination, use `alt=""` for the image. Ensure interactive elements have distinct focus states using `:focus-visible`.
## 2026-06-06 - Added aria-label to inputs relying on placeholders
**Learning:** Screen readers and accessibility tools may not correctly identify inputs that only use a `placeholder` attribute without a visible `<label>`.
**Action:** Always add an `aria-label` attribute to inputs and selects that lack a visible `<label>` tag to ensure proper accessibility without disrupting the existing layout.
