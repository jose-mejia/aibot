# Frontend Brain Dump: Persistent Context

## 2026-01-06: Admin Panel API Integration
- **Session Summary**: Integrated all major Admin Panel pages (`Accounts`, `RegisterUser`, `MT5Connections`, `AuditLogs`, `SignalMonitor`) with the Rust API. Switched from mock authentication to real JWT-based auth via `api.ts`.
- **Challenges & Roadblocks**: 
    - Type mismatch between frontend interfaces and the Backend V2 architecture (specifically `ActiveTrade` model vs the old `Signal` interface).
    - Handling 404/Disconnected states for MT5 status across multiple users without crashing the dashboard.
- **Key Learnings**: 
    - The `X-App-Type` header is mandatory for backend role filtering during login.
    - Glass-panel UI specs must be handled carefully to maintain visibility in Dark Mode.
- **Context for Successors**: 
    - Dashboard polling is currently set to 5-10 seconds.
    - All API logic must go through `api.ts` to ensure consistent header injection and error handling (security hardening).
