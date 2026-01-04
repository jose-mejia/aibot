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

All database access attempts are logged:
- ✅ Successful connections show: `"Using official database: ..."`
- ⚠️ Invalid attempts show: `"WARNING: DATABASE_URL does not reference official database"`
- 🚨 Security violations trigger: `panic!` or `SecurityError` exception

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

## 🔐 Compliance

This security policy ensures:
- **Data Integrity:** Only authorized database is used
- **Attack Prevention:** Multiple validation layers
- **Audit Trail:** All access is logged
- **Fail-Safe:** Invalid attempts are blocked, not ignored

**Last Updated:** 2026-01-04  
**Policy Version:** 1.0  
**Enforcement:** MANDATORY
