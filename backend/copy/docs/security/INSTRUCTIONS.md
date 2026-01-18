# AI Protocols: Security & Auditing

Whenever you (the AI Agent) are tasked with working in this directory or analyzing project security, you must follow these protocols:

## 1. Contextual Awareness
- Theme: **Security Hardening (API, JWT, Logging)**.
- Goal: Ensure **Zero-Trust** communication between Python apps and the Rust API.
- Focus: Validate HMAC signatures, sanitize inputs, and prevent IDOR/XSS.

## 2. Documentation Hygiene
- **Improve the documentation**: Update `docs/security/` files (e.g., `SECURITY_ARCHITECTURE.md`) whenever a new security measure is added.
- Document any new audit event types in the logging schema.

## 3. Experience & Memory (Brain Dump)
- Record your session in `docs/brain/SECURITY_BRAIN.md`.
- Append entries discussing detected vulnerabilities (if any), hardening results, and threat model updates.

---
*Maintaining a bulletproof core for ZulFinance operations.*
