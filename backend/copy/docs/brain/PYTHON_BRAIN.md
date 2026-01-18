# Python Core Brain Dump: Persistent Context

## 2026-01-06: MT5 Automation & Path Validation
- **Session Summary**: Refined the `mt5_path` loading logic to prevent "Wrong Account" errors. Checked that terminal paths are correctly propagated from the local configuration to the Rust API for monitoring.
- **Challenges & Roadblocks**: 
    - Handling multiple MT5 terminal instances on the same machine without port conflicts.
    - Synchronizing local `.env` variables with the central Admin Panel settings.
- **Key Learnings**: 
    - The `numpy` dependency is sensitive to the Python version; using a virtual environment is mandatory for consistent signal detection.
- **Context for Successors**: 
    - The Python apps act as "dumb" bridges that follow the Rust API's lifecycle rules. Always verify an order's status in the API before attempting a local MT5 operation.
