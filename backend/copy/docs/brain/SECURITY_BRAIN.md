# Security Brain Dump: Persistent Context

## 2026-01-06: Security Protocol Hardening
- **Session Summary**: Established mandatory HMAC validation for all Python-to-Rust signal requests. Refined the centralized `log_audit` mechanism in the backend. 
- **Challenges & Roadblocks**: 
    - Ensuring timestamp synchronization between clients and the server to prevent replay attacks without causing false negatives due to minor jitter.
- **Key Learnings**: 
    - Secure HTTP headers (CSP, HSTS) are essential to protect the Admin Panel's glass-morphism effects from clickjacking in embedded scenarios.
- **Context for Successors**: 
    - The `validate_signature` function in `security.rs` is the single source of truth for request authenticity. Never bypass it.
