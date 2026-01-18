# Dashboard Integration Guide - All Roles

## Overview

This guide provides complete information about all three dashboards (Client, Master, Admin) for API integration.

---

## Dashboard Locations

### 1. Client Dashboard
**Path:** `admin_panel_test\client\src\pages\DashboardClient.tsx`
**Target App:** `client_copier\gui` (Desktop App)
**Role:** CLIENT

### 2. Master Dashboard
**Path:** `admin_panel_test\client\src\pages\DashboardMaster.tsx`
**Target App:** `master_sender\gui` (Desktop App)
**Role:** MASTER

### 3. Admin Dashboard
**Path:** `admin_panel_test\client\src\pages\DashboardAdmin.tsx`
**Target App:** Web-only (no desktop version planned)
**Role:** ADMIN

---

## Common Dependencies (All Dashboards)

### Required Components
```
src/components/
├── DashboardLayout.tsx        # Main layout with sidebar
├── ErrorBoundary.tsx          # Error handling
└── ui/                        # shadcn/ui components
    ├── button.tsx
    ├── input.tsx
    ├── avatar.tsx
    └── sonner.tsx
```

### Required Contexts
```
src/contexts/
├── AuthContext.tsx            # Real authentication (replace MockAuth)
└── ThemeContext.tsx           # Theme management
```

### Required Styles
```
src/index.css                  # Complete "Deep Ocean Glass" theme
```

### NPM Packages
```bash
npm install lucide-react sonner wouter
```

---

## Dashboard Comparison

| Feature | Client | Master | Admin |
|---------|--------|--------|-------|
| **Balance Cards** | ✅ | ✅ | ✅ |
| **Recent Trades** | ✅ | ✅ | ✅ |
| **Performance Metrics** | ✅ | ✅ | ✅ |
| **Signal Stats** | ❌ | ✅ | ✅ |
| **User Management** | ❌ | ❌ | ✅ |
| **System Status** | ❌ | ❌ | ✅ |
| **Desktop App** | ✅ | ✅ | ❌ |

---

## API Endpoints Required

### Common Endpoints (All Roles)

#### 1. Account Balance
```typescript
GET /api/account/balance
Headers: { Authorization: Bearer <token> }

Response: {
    balance: number;
    equity: number;
    margin: number;
    free_margin: number;
    margin_level: number;
}
```

#### 2. Recent Trades
```typescript
GET /api/trades/recent?limit=10
Headers: { Authorization: Bearer <token> }

Response: Trade[]

interface Trade {
    ticket: number;
    symbol: string;
    type: 'BUY' | 'SELL';
    volume: number;
    open_price: number;
    close_price?: number;
    profit: number;
    sl?: number;
    tp?: number;
    open_time: string;
    close_time?: string;
    status: 'OPEN' | 'CLOSED';
}
```

#### 3. Performance Metrics
```typescript
GET /api/account/metrics
Headers: { Authorization: Bearer <token> }

Response: {
    total_trades: number;
    win_rate: number;
    profit_factor: number;
    total_profit: number;
    total_loss: number;
}
```

### Master-Specific Endpoints

#### 4. Signal Statistics
```typescript
GET /api/signals/stats
Headers: { Authorization: Bearer <token> }

Response: {
    total_signals: number;
    active_signals: number;
    followers_count: number;
    success_rate: number;
}
```

#### 5. Active Followers
```typescript
GET /api/followers/active
Headers: { Authorization: Bearer <token> }

Response: Follower[]

interface Follower {
    username: string;
    mt5_id: string;
    status: 'ACTIVE' | 'INACTIVE';
    connected_at: string;
}
```

### Admin-Specific Endpoints

#### 6. System Status
```typescript
GET /api/admin/system/status
Headers: { Authorization: Bearer <token> }

Response: {
    api_status: 'ONLINE' | 'OFFLINE';
    database_status: 'CONNECTED' | 'DISCONNECTED';
    mt5_connections: number;
    active_users: number;
    uptime: number;
}
```

#### 7. All Users
```typescript
GET /api/admin/users
Headers: { Authorization: Bearer <token> }

Response: User[]

interface User {
    id: number;
    username: string;
    role: 'CLIENT' | 'MASTER' | 'ADMIN';
    status: 'ACTIVE' | 'INACTIVE';
    mt5_id: string;
    created_at: string;
}
```

---

## Integration Pattern (All Dashboards)

### Step 1: Replace Mock Auth

**Current (Test):**
```tsx
import { useMockAuth } from "@/contexts/MockAuthContext";

const { user } = useMockAuth();
```

**Production:**
```tsx
import { useAuth } from "@/contexts/AuthContext";

const { user, token } = useAuth();
```

### Step 2: Add State Management

```tsx
const [balance, setBalance] = useState<BalanceData | null>(null);
const [trades, setTrades] = useState<Trade[]>([]);
const [metrics, setMetrics] = useState<Metrics | null>(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
```

### Step 3: Load Data on Mount

```tsx
useEffect(() => {
    loadDashboardData();
}, []);

const loadDashboardData = async () => {
    try {
        setLoading(true);
        
        const [balanceData, tradesData, metricsData] = await Promise.all([
            api.getBalance(token),
            api.getRecentTrades(token),
            api.getMetrics(token)
        ]);
        
        setBalance(balanceData);
        setTrades(tradesData);
        setMetrics(metricsData);
    } catch (err) {
        setError('Failed to load dashboard data');
        toast.error('Failed to load dashboard data');
    } finally {
        setLoading(false);
    }
};
```

### Step 4: Add Real-Time Updates (Optional)

```tsx
useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/trades?token=${token}`);
    
    ws.onmessage = (event) => {
        const update = JSON.parse(event.data);
        
        if (update.type === 'TRADE_UPDATE') {
            setTrades(prev => [update.trade, ...prev].slice(0, 10));
        }
        
        if (update.type === 'BALANCE_UPDATE') {
            setBalance(update.balance);
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    return () => ws.close();
}, [token]);
```

### Step 5: Add Loading State

```tsx
if (loading) {
    return (
        <DashboardLayout role={user?.role} username={user?.username}>
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full" />
            </div>
        </DashboardLayout>
    );
}

if (error) {
    return (
        <DashboardLayout role={user?.role} username={user?.username}>
            <div className="text-center text-red-400">
                {error}
            </div>
        </DashboardLayout>
    );
}
```

---

## Complete Integration Example

### Client Dashboard Integration

```tsx
import { useState, useEffect } from 'react';
import DashboardLayout from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";
import { api } from "@/services/api";
import { toast } from 'sonner';

export default function DashboardClient() {
    const { user, token } = useAuth();
    const [balance, setBalance] = useState(null);
    const [trades, setTrades] = useState([]);
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDashboardData();
        
        // WebSocket for real-time updates
        const ws = new WebSocket(`ws://localhost:8000/ws/trades?token=${token}`);
        ws.onmessage = (event) => {
            const update = JSON.parse(event.data);
            if (update.type === 'TRADE_UPDATE') {
                setTrades(prev => [update.trade, ...prev].slice(0, 10));
            }
        };
        
        return () => ws.close();
    }, []);

    const loadDashboardData = async () => {
        try {
            const [balanceData, tradesData, metricsData] = await Promise.all([
                api.getBalance(token),
                api.getRecentTrades(token),
                api.getMetrics(token)
            ]);
            
            setBalance(balanceData);
            setTrades(tradesData);
            setMetrics(metricsData);
        } catch (error) {
            toast.error('Failed to load dashboard data');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <DashboardLayout role="CLIENT" username={user?.username}>
                <div className="flex items-center justify-center min-h-[60vh]">
                    <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full" />
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout role="CLIENT" username={user?.username}>
            {/* Use balance, trades, metrics here */}
            {/* Same UI structure as test version */}
        </DashboardLayout>
    );
}
```

---

## File Structure After Integration

### Client App (client_copier/gui)
```
src/
├── pages/
│   └── dashboards/
│       └── DashboardClient.tsx    ← Integrated
├── components/
│   └── DashboardLayout.tsx        ← Copied from test
├── contexts/
│   └── AuthContext.tsx            ← Real auth (not mock)
├── services/
│   └── api.ts                     ← Real API calls
└── index.css                      ← Theme copied from test
```

### Master App (master_sender/gui)
```
src/
├── pages/
│   └── dashboards/
│       └── DashboardMaster.tsx    ← Integrated
├── components/
│   └── DashboardLayout.tsx        ← Copied from test
├── contexts/
│   └── AuthContext.tsx            ← Real auth (not mock)
├── services/
│   └── api.ts                     ← Real API calls
└── index.css                      ← Theme copied from test
```

### Admin Web App (admin_panel - future)
```
src/
├── pages/
│   └── DashboardAdmin.tsx         ← Integrated
├── components/
│   └── DashboardLayout.tsx        ← Copied from test
├── contexts/
│   └── AuthContext.tsx            ← Real auth (not mock)
├── services/
│   └── api.ts                     ← Real API calls
└── index.css                      ← Theme copied from test
```

---

## Testing Checklist (All Dashboards)

After integration, verify:

**Data Loading:**
- [ ] Balance displays correctly
- [ ] Recent trades populate
- [ ] Metrics calculate properly
- [ ] Loading state shows while fetching
- [ ] Error handling works

**Real-Time Updates:**
- [ ] New trades appear automatically
- [ ] Balance updates in real-time
- [ ] WebSocket connection stable

**UI/UX:**
- [ ] Theme matches test version
- [ ] Responsive on all screen sizes
- [ ] Sidebar navigation works
- [ ] Logout button functions
- [ ] Toast notifications appear

**Performance:**
- [ ] Dashboard loads in < 2 seconds
- [ ] No memory leaks
- [ ] WebSocket reconnects on disconnect

---

## API Service Template

Create `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000';

export const api = {
    async getBalance(token: string) {
        const response = await fetch(`${API_BASE_URL}/api/account/balance`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch balance');
        return response.json();
    },

    async getRecentTrades(token: string, limit = 10) {
        const response = await fetch(`${API_BASE_URL}/api/trades/recent?limit=${limit}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch trades');
        return response.json();
    },

    async getMetrics(token: string) {
        const response = await fetch(`${API_BASE_URL}/api/account/metrics`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch metrics');
        return response.json();
    },

    // Master-specific
    async getSignalStats(token: string) {
        const response = await fetch(`${API_BASE_URL}/api/signals/stats`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch signal stats');
        return response.json();
    },

    // Admin-specific
    async getSystemStatus(token: string) {
        const response = await fetch(`${API_BASE_URL}/api/admin/system/status`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch system status');
        return response.json();
    }
};
```

---

## Quick Reference

**Test Environment (Source):**
```
admin_panel_test/client/src/pages/
├── DashboardClient.tsx    → Copy to client_copier/gui
├── DashboardMaster.tsx    → Copy to master_sender/gui
└── DashboardAdmin.tsx     → Copy to admin web app
```

**What to Keep:**
- ✅ All UI components and styling
- ✅ Layout structure
- ✅ Component hierarchy
- ✅ Theme (Deep Ocean Glass)

**What to Replace:**
- ❌ MockAuthContext → Real AuthContext
- ❌ Static data arrays → API calls
- ❌ Manual refresh → WebSocket updates

---

## Support

For questions:
- **Styling:** See `docs/frontend/COMPONENTS.md`
- **API Integration:** See `docs/frontend/DEVELOPMENT_GUIDE.md`
- **Theme:** See `index.css` in test version
- **Routing:** See `App.tsx` in test version
