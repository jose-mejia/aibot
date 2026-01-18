# 🏗️ Database & API Architecture V2: Active vs. History Separation

## 🎯 Objective
Eliminate "Zombie Execution" risks (re-opening old trades) and improve system performance by strictly separating **Active Execution State** from **Historical Reporting Data**.

---

## 🛑 Core Principles
1.  **Hot vs. Cold Data Isolation:**
    *   **Hot Data (Active):** Only trades currently open and managed by the bot. Optimized for speed and concurrency.
    *   **Cold Data (History):** Closed trades. Immutable for the bot core. Optimized for reporting and analysis.
2.  **Zero-Trust On Restart:**
    *   The Client Copier/Service relies **ONLY** on the `Active` table/endpoint during startup.
    *   The `History` table is **NEVER** queried for execution decisions.
3.  **Atomic Lifecycle Transitions:**
    *   A trade MUST NOT exist in both states simultaneously (except transiently during the exact moment of closure transition).

---

## 🗄️ Database Schema Design (Conceptual)

### 1. `active_trades` (The Hot Table)
*   **Purpose:** Live execution state.
*   **Source of Truth:** For the Client Sidecar/Copier.
*   **Retention:** Rows are DELETED immediately after the trade is closed.

```json
{
  "ticket_id": "123456",
  "master_ticket": "987654",
  "symbol": "EURUSD",
  "volume": 0.01,
  "direction": "BUY",
  "open_price": 1.1050,
  "sl": 1.1000,
  "tp": 1.1200,
  "created_at": "2024-01-01T10:00:00Z",
  "status": "OPEN"
}
```

### 2. `trade_history` (The Cold Table)
*   **Purpose:** Reporting, Dashboards, and Audit logs.
*   **Source of Truth:** For the Frontend UI (History Tab) and User Reports.
*   **Retention:** Permanent (until manual purge).

```json
{
  "history_id": "uuid-v4",
  "ticket_id": "123456",     // Copied from Active
  "master_ticket": "987654", // Copied from Active
  "symbol": "EURUSD",
  "close_price": 1.1100,
  "profit": 5.00,
  "open_time": "...", 
  "close_time": "2024-01-01T12:00:00Z",
  "reason": "TP_HIT"
}
```

---

## 🔌 API Endpoint Requirements (Backend)

The Backend API must expose distinct endpoints to enforce this separation.

### Execution Endpoints (For Client Copier / Python Sidecar)
*   `GET /api/v2/trades/active`  **(🔥 HOT Endpoint)**
    *   **Returns:** Only open trades (Active Execution State).
    *   **Rule:** The Python Client **MUST ONLY** poll this endpoint. It is forbidden from accessing history.
    *   **Usage:** Sync on startup. If it's not here, the bot ignores it.
*   `POST /api/v2/trades/active`
    *   **Usage:** Report a new trade opened.
*   `DELETE /api/v2/trades/active/{ticket}`
    *   **Usage:** Close/Remove a trade from active state. **Triggers atomic movement to history.**

### Reporting Endpoints (For Frontend UI Only)
*   `GET /api/v2/trades/history` **(❄️ COLD Endpoint)**
    *   **Returns:** Paginated list of closed trades (Archive).
    *   **Rule:** The Python Client **NEVER** touches this. Only for React/Frontend reporting.
    *   **Usage:** Populating the "History" tab in the dashboard.
    *   **Filter:** specific dates, symbols, etc.

---

## 🔄 Lifecycle Flow (The "Transition")

1.  **Signal Received (OPEN):**
    *   Master sends NEW_TRADE.
    *   Client opens execution.
    *   Client POSTs to `/active`.
2.  **Trade Management:**
    *   Client queries/updates `/active` for modifications (SL/TP).
3.  **Signal Received (CLOSE) or TP/SL Hit:**
    *   Client closes execution in MT5.
    *   Client calls `DELETE /active/{ticket}` (or `POST /close` depending on implementation preference).
    *   **Backend Action:**
        1.  Read trade data from `active_trades`.
        2.  Insert into `trade_history` with close details.
        3.  Delete from `active_trades`.
        4.  (Transaction Commit).

---

## 🛡️ Safety Guarantee
By design, if the Client Copier restarts:
1.  It asks: "What is Active?" (`GET /active`).
2.  API responds: "Only these 2 trades are open."
3.  Everything else (even if it happened 1 second ago and caused a crash) is in History (or deleted), invisible to the execution logic.
**Result:** Impossible to re-open a closed trade.
