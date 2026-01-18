# Backend Brain Dump: Persistent Context

## 2026-01-06: API Synchronization & Security
- **Session Summary**: Verified compatibility with the React Admin Panel. The Rust API now serves real data for `audit_logs`, `dashboard_stats`, `mt5_connections`, and `active_trades`.
- **Challenges & Roadblocks**: 
    - Ensuring atomic transitions during signal closure (moving from `active_trades` to `trade_history`).
    - Managing in-memory cache for MT5 status (`MT5_CACHE`) to avoid excessive DB reads for balance monitoring.
- **Key Learnings**: 
    - The middleware for secure HTTP headers is critical for preventing unauthorized iframe injection of the admin panel.
- **Context for Successors**: 
    - The `V2` architecture separates hot storage for trading logic and cold storage for frontend reports. Always check if an operation belongs to `v2` handlers.
