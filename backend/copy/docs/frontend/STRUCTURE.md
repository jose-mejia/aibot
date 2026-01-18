# Project Structure & Architecture

This document describes the structure of the ZulFinance Admin Panel, which serves as the unified interface for Clients, Masters, and Administrators.

## Directory Overview (api_server/admin_panel)

- `src/`: Core source directory.
  - `components/`: UI components and layout logic.
    - `ui/`: Design system based on shadcn/ui primitives.
    - `DashboardLayout.tsx`: The primary Shell for authenticated routes (w-64 sidebar).
  - `contexts/`: React Contexts for global state.
    - `AuthContext.tsx`: **Production-ready** authentication logic (JWT).
    - `ThemeContext.tsx`: Theme switching and glassmorphism tokens.
  - `pages/`: Page-level components organized by access level.
    - `admin/`: Restricted pages only for ADMIN role (User mgmt, System status).
    - `DashboardClient.tsx`: Main view for Follower accounts.
    - `DashboardMaster.tsx`: Control panel for Signal Providers.
    - `DashboardAdmin.tsx`: Executive overview for system admins.
    - `LandingPage.tsx`: The website/root portal (`/`).
    - `LoginPage.tsx`: Premium design gateway.
  - `services/`: Backend communication layer.
    - `api.ts`: Fetch-based API client with real endpoints.
  - `App.tsx`: Main Entry/Routing. Handles the `SmartRouter` logic for role-based redirects.

## Authentication & Authorization

- **AuthContext**: Replaced the legacy `MockAuth` with a real JWT-based provider.
- **SmartRouter**: Located in `App.tsx`, it automatically redirects users to their specific dashboard after login based on their `role` (ADMIN, MASTER, CLIENT).
- **Protected Routes**: Navigation in `DashboardLayout` is filtered dynamically using the user's role.

## Design System: "Deep Ocean Glass"

The project uses a custom aesthetic characterized by:
- **Glassmorphism**: High `backdrop-blur`, semi-transparent backgrounds (`bg-white/5`), and subtle borders.
- **Neon Glows**: Targeted use of `blur-xl` and cyan/primary gradients for high-impact elements (Login button, active icons).
- **Responsive Shell**: Sidebar-based navigation that collapses into a bottom/sheet bar on mobile.

## Routing Strategy

Used `wouter` for its lightweight overhead:
1. Root (`/`) -> `LandingPage` (Website).
2. `/login` -> `LoginPage` (Gateway).
3. `/dashboard-*` -> Authenticated Shell using `DashboardLayout`.

---
*Note: This structure was fused from the original prototype to include full backend integration.*
