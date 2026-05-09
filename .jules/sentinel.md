## 2024-05-09 - Missing Authentication on Sensitive Endpoints
**Vulnerability:** Several sensitive API endpoints (e.g., `create_labour`, `update_material_endpoint`, `delete_site`, etc.) were accessible without authentication because the `Depends(get_current_user)` dependency was omitted.
**Learning:** Forgetting to apply authentication dependencies to new or updated routes can leave an entire sub-system exposed to unauthenticated users. This is a common oversight in FastAPI when standardizing routing without a central router configuration.
**Prevention:** Always verify that every sensitive route includes the `Depends(get_current_user)` parameter. Consider applying the dependency globally via an `APIRouter` to ensure all contained routes are protected by default.
