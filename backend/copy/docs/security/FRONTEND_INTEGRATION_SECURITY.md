# 🔒 Frontend-Backend Integration Security

**Version:** 1.0  
**Last Updated:** 2026-01-05  
**Status:** AUDITED & SECURE  

---

## 🏗️ Integration Architecture

The Zulfinance system uses a multi-application frontend architecture where separate Tauri apps for **Master Sender** and **Client Copier** interact with a centralized **Rust API Server**.

### Security Flow: Login & Authentication

1.  **Application Identification:** Each frontend app identifies itself via the `X-App-Type` header during login (e.g., `desktop-client` or `desktop-master`).
2.  **Role Restriction (Backend Enforcement):**
    - `desktop-client` -> Only users with role `FOLLOWER` are permitted.
    - `desktop-master` -> Only users with role `MASTER` are permitted.
    - **Security Benefit:** Prevents a client from logging into the Master app to forge signals.
3.  **Token Issuance:** Upon success, the server returns a JWT (24h expiry).
4.  **Secure Storage:** The frontend stores the token in `sessionStorage`. 
    - **Security Benefit:** Token is volatile and cleared automatically when the app/window is closed.

---

## 🌐 Web Admin Panel Security (V2)

The modern React Admin Panel implements enterprise-grade security for browser-based operations.

### 1. Hardened Security Headers (Backend-Enforced)
Implemented in `src/security.rs`, the API server sends additional headers to protect the browser session:
- **`Content-Security-Policy` (CSP):** Mitigates XSS by strictly defining allowed content sources.
- **`X-Frame-Options: DENY`:** Prevents the dashboard from being embedded in malicious iframes (Clickjacking).
- **`Referrer-Policy: strict-origin-when-cross-origin`:** Ensures no sensitive path data leaks to external links.

### 2. Activity-Based Session Preservation
To balance security with usability, the 15-minute idle timer is synchronized with the API:
- **UI Events:** Mouse movements, clicks, and keyboard actions reset the timer.
- **API Activity:** Every successful response from the backend emits a `session-activity` event, keeping the user logged in while they are actively viewing or modifying data.

### 3. Global Security Interceptor
Instead of individual component logic, `api.ts` uses a centralized `request` helper:
- **Automatic Cleanup:** If the server returns a `401 Unauthorized` or `403 Forbidden` (e.g., token revoked or role changed), the frontend **immediately** wipes the token from `sessionStorage` and redirects to the Login page.

---

## 🐍 Sidecar Security (Python Integration)

The frontend manages the lifecycle of the Python trading engine (Sidecar) with strict security boundaries.

### 1. Token Delegation
Instead of passing user credentials, the frontend passes the JWT token to the sidecar via command-line arguments:
```bash
client-service.exe --token "eyJhbGciOiJIUzI1Ni..."
```
**Security Benefit:** Python process never sees or stores user passwords.

### 2. Kill Switch Implementation
The Tauri `appWindow` listens for close events to ensure the sidecar dies with the GUI:
```typescript
// src/App.tsx
appWindow.listen("tauri://close-requested", async () => {
    await stopPythonService(); // Force kill sidecar
    sessionStorage.clear();    // Wipe session
});
```

---

## 🛰️ API Communication

### Protected Routes
All requests to `/signals`, `/api/v2/actives`, and `/users/me` include the Bearer token:
```http
Authorization: Bearer <JWT_TOKEN>
```

### Automatic Session Termination
- **Unauthorized (401):** The frontend interceptor automatically clears the session and returns the user to the Login screen if the token is revoked or expired.
- **Inactivity:** Auto-logout is enforced after 15 minutes of inactivity.

---

## 🔄 V2 Architecture Adoption

### Signal Retrieval
- The frontend currently utilizes the `/signals` endpoint.
- **Security Alignment:** The backend internally maps this route to the `active_trades` table (V2 Architecture), ensuring the "Zombie Order" protection is enforced even on legacy routes.

---

## 📋 Integration Audit Checklist

- [x] `X-App-Type` header implemented in login service
- [x] JWT Token storage moved to `sessionStorage`
- [x] Sidecar successfully receives token via CLI args
- [x] Kill switch verified on app close
- [x] 401 error handler redirects to login
- [x] 15m idle auto-logout implemented
- [x] V1 routes correctly mapped to V2 DB logic

---

## 🚨 Secure Development Mandates

1.  **Never** store tokens in `localStorage` for production versions.
2.  **Never** log the full JWT token in the console (logs are sanitized).
3.  **Always** ensure the sidecar is stopped before app exit.
4.  **Maintain** parity between Master and Client GUI security logic.

---

**END OF INTEGRATION SECURITY DOCUMENT**
