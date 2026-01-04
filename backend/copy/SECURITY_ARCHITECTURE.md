# 🔒 ZulFinance Trade Copier - Security Architecture

**Version:** 1.0  
**Last Updated:** 2026-01-02  
**Status:** MANDATORY - DO NOT MODIFY WITHOUT REVIEW

---

## ⚠️ CRITICAL NOTICE

**THIS DOCUMENT DEFINES THE SECURITY FOUNDATION OF THE ZULFINANCE SYSTEM.**

Before making ANY changes to authentication, authorization, data transmission, or session management:

1. **READ THIS DOCUMENT COMPLETELY**
2. **UNDERSTAND THE THREAT MODEL**
3. **ENSURE YOUR CHANGES MAINTAIN OR IMPROVE SECURITY**
4. **NEVER DOWNGRADE SECURITY FOR CONVENIENCE**

---

## 🎯 Security Objectives

### Primary Goals
1. **Prevent Unauthorized Trading:** Only authenticated, paid users can execute trades
2. **Prevent Signal Forgery:** Only legitimate Master accounts can broadcast signals
3. **Prevent Replay Attacks:** Intercepted packets cannot be reused
4. **Prevent Data Tampering:** Signal data cannot be modified in transit
5. **Enforce Session Validity:** Expired or revoked sessions must immediately stop trading

### Threat Model

**Attackers We Defend Against:**
- **Script Kiddies:** Trying to run the copier without paying
- **Reverse Engineers:** Extracting credentials from binaries
- **Man-in-the-Middle:** Intercepting and modifying signals
- **Replay Attackers:** Reusing captured valid requests
- **Token Thieves:** Stealing JWT tokens to impersonate users

---

## 🏗️ Architecture Overview

```
┌─────────────────┐
│  React Frontend │ (Tauri Desktop App)
│   (Login UI)    │
└────────┬────────┘
         │ 1. Login (username/password)
         ▼
┌─────────────────┐
│   API Server    │ (Rust - Port 8000)
│  (Gatekeeper)   │
└────────┬────────┘
         │ 2. Returns JWT Token + validates payment
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────┐
│ Master  │ │  Client  │ (Python Services)
│ Sender  │ │  Copier  │
└─────────┘ └──────────┘
    │            │
    │ 3. Uses Token for ALL API calls
    │            │
    └────────────┘
```

---

## 🔐 Security Layers

### Layer 1: Authentication (Who are you?)

#### Frontend (React/Tauri)
- **Login Form:** Collects `username` and `password`
- **API Call:** `POST /token` with form-urlencoded credentials
- **Response:** JWT Token (if valid) or 401 (if invalid)
- **Storage:** Token stored in React state (memory only, NOT localStorage)

#### API Server (Rust)
- **Endpoint:** `POST /token`
- **Validation:**
  1. Check if user exists in database
  2. Verify password using `bcrypt::verify()`
  3. Check if user status is `ACTIVE` (not suspended/expired)
  4. Check if payment is valid (subscription active)
- **Token Generation:**
  ```rust
  let claims = Claims {
      sub: user.username,
      exp: now + 24h,
      role: user.role,
      mt5_id: user.allowed_mt5_id
  };
  let token = encode(&Header::default(), &claims, &EncodingKey::from_secret(SECRET_KEY))?;
  ```

**🚨 SECURITY RULE 1:** Passwords MUST be hashed with bcrypt (cost factor ≥ 12)

**🚨 SECURITY RULE 2:** Tokens MUST expire (max 24 hours)

---

### Layer 2: Authorization (What can you do?)

#### Token Injection (Python Services)

**CRITICAL PRINCIPLE:** Python services NEVER store credentials. They receive a token from the frontend.

**Client Copier:**
```bash
python main_client.py --token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Master Sender:**
```bash
python main_sender.py --token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Implementation:**
```python
class ClientService:
    def __init__(self, config, token):
        self.token = token
        if not self.token:
            logger.critical("SECURE MODE: No Auth Token provided. Terminating.")
            sys.exit(1)
```

**🚨 SECURITY RULE 3:** Python services MUST terminate immediately if no token is provided

**🚨 SECURITY RULE 4:** Config files MUST NOT contain API credentials (username/password)

---

### Layer 3: Transport Security (Is the data safe?)

#### HTTPS/TLS (Production)
- **Requirement:** All API communication MUST use HTTPS in production
- **Certificate:** Valid TLS certificate (Let's Encrypt or commercial)
- **Minimum Version:** TLS 1.2 (prefer TLS 1.3)

#### Bearer Token Authentication
All API requests include:
```
Authorization: Bearer <JWT_TOKEN>
```

**🚨 SECURITY RULE 5:** Tokens MUST be transmitted via Authorization header (never in URL)

---

### Layer 4: Data Integrity (Has the data been tampered?)

#### HMAC-SHA256 Payload Signing (Master Sender)

**Purpose:** Prevent signal forgery and tampering

**Implementation:**
```python
def _get_headers(self, payload=None):
    headers = {"Authorization": f"Bearer {self.token}"}
    
    if payload:
        # 1. Timestamp (anti-replay)
        timestamp = str(int(time.time() * 1000))
        headers["X-Timestamp"] = timestamp
        
        # 2. Canonical string
        payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        canonical = f"{timestamp}.{payload_str}"
        
        # 3. HMAC signature
        signature = hmac.new(
            self.token.encode('utf-8'),
            canonical.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers["X-Signature"] = signature
    
    return headers
```

**API Server Validation (Rust - TO IMPLEMENT):**
```rust
// 1. Extract timestamp and signature from headers
let timestamp = req.headers().get("X-Timestamp")?;
let signature = req.headers().get("X-Signature")?;

// 2. Verify timestamp is recent (within 10 seconds)
let now = SystemTime::now().duration_since(UNIX_EPOCH)?.as_millis();
if (now - timestamp.parse::<u128>()?) > 10000 {
    return Err(StatusCode::FORBIDDEN); // Replay attack
}

// 3. Reconstruct canonical string
let body_str = serde_json::to_string(&body)?;
let canonical = format!("{}.{}", timestamp, body_str);

// 4. Compute expected signature
let expected = hmac_sha256(&token, &canonical);

// 5. Compare (constant-time to prevent timing attacks)
if !constant_time_eq(signature, expected) {
    return Err(StatusCode::FORBIDDEN); // Tampered data
}
```

**🚨 SECURITY RULE 6:** All Master Sender signals MUST include X-Signature and X-Timestamp headers

**🚨 SECURITY RULE 7:** API Server MUST reject requests with invalid signatures or stale timestamps (>10s)

---

### Layer 5: Session Management (Is the session still valid?)

#### WebSocket Authentication (Client Copier)

**Connection:**
```python
uri = f"{self.ws_url}/ws?token={self.token}"
async with websockets.connect(uri) as websocket:
    # Listen for signals
```

**API Server Validation:**
```rust
async fn ws_handler(
    ws: WebSocketUpgrade,
    Query(params): Query<HashMap<String, String>>,
) -> Response {
    let token = params.get("token").ok_or(StatusCode::UNAUTHORIZED)?;
    
    // Validate JWT
    let claims = decode_token(token)?;
    
    // Check user status in database
    let user = db.get_user(&claims.sub).await?;
    if user.status != "ACTIVE" {
        return Err(StatusCode::FORBIDDEN); // Suspended account
    }
    
    ws.on_upgrade(|socket| handle_socket(socket, claims))
}
```

#### Kill Switch Mechanism

**Server-Side:**
- Periodic check (every 60s) if user is still active/paid
- If not, send `{"event": "STOP"}` via WebSocket and close connection

**Client-Side:**
```python
async def handle_signal(self, payload):
    event = payload.get("event")
    
    if event == "STOP":
        logger.critical("RECEIVED STOP COMMAND FROM SERVER. SHUTTING DOWN.")
        self.close_all_and_exit()
```

**🚨 SECURITY RULE 8:** Client MUST immediately terminate on STOP command

**🚨 SECURITY RULE 9:** Client MUST terminate on WebSocket close with auth error codes (4001, 1008)

---

### Layer 6: Anti-Reverse Engineering (Can they extract secrets?)

#### Token Injection (No Hardcoded Secrets)
- ✅ **CORRECT:** Token passed as CLI argument
- ❌ **WRONG:** Token/password in config.json

#### Binary Obfuscation (Future - .exe build phase)
- PyArmor for Python obfuscation
- Nuitka for native compilation
- Tauri for final packaging

**🚨 SECURITY RULE 10:** NEVER commit tokens, passwords, or SECRET_KEY to version control

---

## 📋 Security Checklist

Before deploying or modifying code, verify:

### Authentication
- [ ] Passwords are bcrypt-hashed (cost ≥ 12)
- [ ] JWT tokens expire (max 24h)
- [ ] Token validation checks user status (ACTIVE)
- [ ] Failed login attempts are logged

### Authorization
- [ ] Python services require --token argument
- [ ] Services terminate if token is missing
- [ ] Config files contain NO credentials
- [ ] Token is passed via Authorization header

### Data Integrity
- [ ] Master Sender signs all payloads with HMAC-SHA256
- [ ] API Server validates signatures
- [ ] Timestamps prevent replay attacks (10s window)

### Session Management
- [ ] WebSocket connections validate JWT on connect
- [ ] Server sends STOP command on subscription expiry
- [ ] Client terminates on STOP or auth errors

### Transport
- [ ] HTTPS enabled in production
- [ ] TLS 1.2+ enforced
- [ ] No sensitive data in URLs

---

## 🚨 Common Security Mistakes to AVOID

### ❌ NEVER DO THIS:
```python
# BAD: Hardcoded credentials
username = "admin"
password = "admin123"

# BAD: Token in config file
config = {"api": {"token": "eyJhbGc..."}}

# BAD: Ignoring auth errors
if response.status_code == 401:
    print("Auth failed, continuing anyway...")  # NO!

# BAD: Storing token in localStorage (XSS risk)
localStorage.setItem('token', token)
```

### ✅ ALWAYS DO THIS:
```python
# GOOD: Token injection
parser.add_argument("--token", required=True)

# GOOD: Terminate on auth failure
if response.status_code == 401:
    logger.critical("Auth failed. Terminating.")
    sys.exit(1)

# GOOD: Memory-only token storage (React state)
const [token, setToken] = useState(null)
```

---

## 🔄 Security Update Process

When updating security:

1. **Document the change** in this file
2. **Update version number** at the top
3. **Test thoroughly** in isolated environment
4. **Verify no security downgrade** occurred
5. **Update all affected components** (Python, Rust, React)

---

## 📞 Security Incident Response

If a security breach is suspected:

1. **Immediately revoke all active tokens** (API Server)
2. **Force password reset** for all users
3. **Audit logs** for suspicious activity
4. **Patch vulnerability** before re-enabling service
5. **Document incident** and update this file

---

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [HMAC-SHA256 Specification](https://tools.ietf.org/html/rfc2104)
- [WebSocket Security](https://datatracker.ietf.org/doc/html/rfc6455#section-10)

---

**END OF SECURITY ARCHITECTURE DOCUMENT**

*This document is the source of truth for ZulFinance security. Treat it as law.*
