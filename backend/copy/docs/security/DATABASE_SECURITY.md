# 🔒 DATABASE SECURITY POLICY

## ⚠️ CRITICAL SECURITY NOTICE

This application uses **ONLY ONE OFFICIAL DATABASE**:

```
api_server/aibot.db
```

**ANY attempt to use a different database is a SECURITY VIOLATION and will be blocked.**

---

## 🏗️ Secure Architecture

### Access Control Model

```
┌─────────────────────────────────────────────────┐
│  Desktop Applications (Master/Client)           │
│  - NO direct database access                    │
│  - Communication via API only                   │
└────────────────┬────────────────────────────────┘
                 │
                 │ HTTPS/WSS (Authenticated)
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  API Server (Rust)                              │
│  ✅ ONLY authorized database accessor           │
│  - Authentication & Authorization               │
│  - Business Logic & Validation                  │
│  - SQL Injection Prevention                     │
└────────────────┬────────────────────────────────┘
                 │
                 │ SQLite (Local File)
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  aibot.db (api_server/)                         │
│  🔒 Protected by filesystem permissions         │
│  🔒 Single point of truth                       │
└─────────────────────────────────────────────────┘
```

**Security Benefits:**
- ✅ **Single Point of Control:** All data access audited
- ✅ **Attack Surface Reduction:** No direct DB exposure
- ✅ **Centralized Validation:** Business rules enforced
- ✅ **Audit Trail:** All operations logged

---

## 🛡️ Security Layers Implemented

### Layer 1: Rust API Server
- **Module:** `src/config.rs`
- **Protection:** Hardcoded database name with validation
- **Blocks:** Path traversal, unauthorized database names
- **Validation:** Runtime checks on database URL

### Layer 2: Python Scripts
- **Module:** `db_config.py`
- **Protection:** Centralized path with SecurityError exceptions
- **Blocks:** Relative paths, path traversal, name mismatches
- **Validation:** Absolute path resolution and verification

### Layer 3: Environment Variables
- **Variable:** `DATABASE_URL` (optional)
- **Protection:** Validated to ensure it references `aibot.db`
- **Fallback:** Always defaults to official database if invalid

### Layer 4: Centralized Audit Logging
- **Module:** `src/handlers/mod.rs` (`log_audit`)
- **Protection:** Write-only (via API) record of all security-sensitive events
- **Storage:** `audit_logs` table
- **Purpose:** Compliance, non-repudiation, and incident forensics

---

## 🚨 Attack Scenarios Prevented

### 1. Path Traversal Attack
```python
# ❌ BLOCKED
db_path = "../../../etc/passwd"
```
**Protection:** Both Rust and Python modules check for `..` in paths.

### 2. Database Substitution
```python
# ❌ BLOCKED
db_path = "api_server/malicious.db"
```
**Protection:** Filename validation ensures only `aibot.db` is accepted.

### 3. Environment Variable Injection
```bash
# ❌ BLOCKED (will fallback to official)
export DATABASE_URL="sqlite:hacked.db"
```
**Protection:** URL is validated to contain `aibot.db`.

### 4. Symbolic Link Attack
```bash
# ❌ BLOCKED
ln -s /tmp/fake.db api_server/aibot.db
```
**Protection:** Absolute path resolution detects symlink targets.

---

## 📋 Developer Guidelines

### ✅ DO:
- Use `db_config.OFFICIAL_DB_PATH` in Python scripts
- Use `config::get_official_db_url()` in Rust code
- Trust the security modules

### ❌ DON'T:
- Hardcode database paths in scripts
- Use relative paths
- Override `OFFICIAL_DB_NAME` constant
- Disable security validations

---

## 🔍 Audit Trail

All system-changing operations are logged to the `audit_logs` table:

### Tracked Events
- **USER_LOGIN:** Successful and failed login attempts (with IP if provided)
- **CREATE_USER:** When an admin creates a new user
- **UPDATE_SETTING:** Changes to global system configurations
- **CREATE_MT5 / DELETE_MT5:** Management of MT5 terminal connections
- **V2_CLOSE:** Atomic transitions between Active and History tables

### Audit Log Schema
| Field | Description |
| :--- | :--- |
| `timestamp` | UTC time of event |
| `action` | Event type (e.g., USER_LOGIN) |
| `username` | Subject or actor username |
| `status` | SUCCESS or FAILURE |
| `details` | Contextual info (e.g., "Invalid password") |

### Compliance
- ✅ Successful actions show: `"SUCCESS"`
- ⚠️ Blocked/Invalid attempts show: `"FAILURE"`
- 🚨 Security violations are strictly logged before any action is blocked.

---

## 🧪 Testing Security

Run the security test:
```bash
python db_config.py
```

Expected output:
```
✅ Official Database Path: C:\...\api_server\aibot.db
✅ Exists: True
```

---

## 📞 Security Incident Response

If you suspect a security breach:
1. **Stop all services immediately**
2. **Check logs for security warnings**
3. **Verify database integrity:** `python debug_db.py`
4. **Review recent code changes**
5. **Contact system administrator**

---

## 🆕 V2 Enhancements (2026-01-05)

### WAL Mode (Write-Ahead Logging)
**Implementation:** `src/db/mod.rs`

```rust
sqlx::query("PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON; PRAGMA synchronous = NORMAL;")
    .execute(&pool)
    .await?;
```

**Security Benefits:**
- **Crash Safety:** Database corruption prevented on power loss/crash
- **Concurrency:** Better read/write performance under load
- **Atomicity:** Enhanced transaction reliability for V2 Active/History split

### Active/History Architecture
See `docs/security/V2_ARCHITECTURE_SECURITY.md` for:
- Zombie Order prevention
- Atomic lifecycle transitions
- Segregated data access patterns

---

## 🔐 Compliance

This security policy ensures:
- **Data Integrity:** Only authorized database is used
- **Attack Prevention:** Multiple validation layers
- **Audit Trail:** All access is logged
- **Fail-Safe:** Invalid attempts are blocked, not ignored
- **Crash Safety:** WAL mode protects against corruption
- **Architectural Security:** V2 split prevents Zombie Orders

**Last Updated:** 2026-01-05  
**Policy Version:** 2.0  
**Enforcement:** MANDATORY
