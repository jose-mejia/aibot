# Client Dashboard Documentation

## Overview
The Client Dashboard (`DashboardClient.tsx`) is the central hub for "Follower" users. It provides real-time visibility into trading performance, signal execution health, and connection status. This document details the data structure and UI components for backend integration.

## 📊 Data Requirements

The dashboard expects a consolidated JSON response. The backend should provide an endpoint (e.g., `GET /api/client/dashboard`) returning the following structure:

```json
{
  "user": {
    "username": "client_demo",
    "role": "FOLLOWER",
    "allowed_mt5_id": 11629107
  },
  "mt5_status": {
    "connected": true,          // Controls the Connect Card state (ONLINE/OFFLINE)
    "server": "XP-Demo",
    "account_id": 11629107,
    "balance": 5234.60,
    "ping": "14ms"
  },
  "signals": {
    "total_received": 45,
    "executed": 42,
    "rejected": 3
  },
  "performance": {
    "pnl_today": 124.50,
    "pnl_week": 456.80,
    "pnl_month": 1234.60,
    "balance_evolution": [      // Array for the chart (Last 7 days)
      { "day": "Mon", "value": 5000.00 },
      { "day": "Tue", "value": 5050.00 },
      { "day": "Wed", "value": 5120.00 },
      { "day": "Thu", "value": 5080.00 },
      { "day": "Fri", "value": 5200.00 },
      { "day": "Sat", "value": 5180.00 },
      { "day": "Sun", "value": 5234.60 }
    ]
  },
  "trading_stats": {
    "total_orders": 42,
    "success_rate": 93.33,
    "avg_execution_time": 145
  },
  "recent_copies": [            // List for the side widget (Last 5 orders)
    {
      "id": 1,
      "symbol": "EURUSD",
      "type": "BUY",
      "lot": 0.10,
      "status": "executed",     // Enum: "executed" | "rejected"
      "pnl": 12.50,             // Signed float
      "time": "2 min ago",
      "reason": null            // Optional string for rejection reason
    }
  ]
}
```

## 🧩 UI Components & Logic

### 1. Header
- **Dynamic Welcome:** Displays `Welcome, {user.username}`.
- **Date Filter:** Currently locked to "Last 7 Days" (visual only).

### 2. Signal Stats (Top Row)
Three cards displaying signal health:
- **Total Received:** All signals targeted to this user.
- **Executed:** Signals successfully converted to orders.
- **Rejected:** Signals blocked (e.g., max spread, risk limits).

### 3. Performance Financial (Main Widget)
- **P&L Summary:** Displays Today, Week, and Month P&L.
- **Styling:** Values >= 0 are Green (Emerald), < 0 are Red (Rose).
- **Balance Evolution Chart:**
  - Interactive bar chart showing equity curve.
  - Shows tooltip with exact value on hover.
  - **Logic:** Heights are calculated relative to min/max values of the period.

### 4. Trading Statistics
- **Total Orders:** Total executed trades.
- **Success Rate:** `(Executed / Total) * 100`.
- **Avg Execution:** Average latency in ms.

### 5. MT5 Connection Card (Right Sidebar)
**Critical Component:** Handles the "Offline" state properly.
- **Logic:**
  - `if (connected)`: Shows Server, Account ID, Balance, Ping. Status badge is `ONLINE` (Green).
  - `else`: Shows "Waiting for Connection" state with disconnected instructions. Status badge is `OFFLINE` (Red).

### 6. Recent Copies (Right Sidebar)
- Lists the last 5 signals processed.
- **Status Icons:** Checkmark for executed, X for rejected.
- **Real-time:** Should update immediately upon new signal.

## 🛠 Integration Guidelines
1. **Mock Replacement:** Locate the `mock*` constants in `DashboardClient.tsx` and replace them with API calls.
2. **Real-time Updates:** Use WebSockets or Polling (every 5s) for:
   - `mt5_status` (Critical for UX)
   - `recent_copies`
   - `performance` (P&L updates)
