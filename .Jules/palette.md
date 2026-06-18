## 2024-04-25 - [Semantic HTML for Dashboard Cards]
**Learning:** Found an accessibility issue pattern specific to this app where dashboard navigation cards were created using `<div>` tags with `onclick` handlers, relying on JavaScript for navigation. This breaks native keyboard navigation, screen reader support, and standard browser actions (like opening in a new tab). Also, using `alt` text identical to visible text in cards causes redundant screen reader announcements.
**Action:** Always prefer semantic HTML elements (like `<a>` for navigation links) over `<div>`s with JavaScript handlers. For images in links where the link text already describes the destination, use `alt=""` for the image. Ensure interactive elements have distinct focus states using `:focus-visible`.

## 2024-11-20 - Standardize Destructive Action Confirmations
**Learning:** The application has a pattern of using native browser `confirm()` dialogs for deleting records (e.g., laborers, inventory items). However, this pattern was inconsistently applied, with some actions (like deleting payments) directly triggering backend API calls. This inconsistency risks accidental data loss.
**Action:** When adding new delete or destructive actions, always implement a native `confirm()` dialog before executing the API request to maintain a consistent UX and prevent user error.
