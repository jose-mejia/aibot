# Client Dashboard - Migration Guide for Desktop App

## Location

**Source Path:** `C:\Users\josemejia\dev\python\aibot\backend\copy\admin_panel_test\client\src\pages\DashboardClient.tsx`

**Target App:** `client_copier\gui` (Tauri Desktop App)

---

## Files to Copy

### Main Dashboard Component

**File:** `DashboardClient.tsx`
**Location:** `admin_panel_test\client\src\pages\DashboardClient.tsx`

This is the complete Client dashboard with:
- Account balance cards
- Recent trades table
- Performance metrics
- "Deep Ocean Glass" styling

### Required Dependencies

**Layout Component:**
- `src\components\DashboardLayout.tsx`

**Context:**
- `src\contexts\AuthContext.tsx`
- `src\contexts\ThemeContext.tsx`

**UI Components (shadcn/ui):**
- `src\components\ui\button.tsx`
- `src\components\ui\input.tsx`
- `src\components\ui\avatar.tsx`
- `src\components\ui\sonner.tsx`

**Styles:**
- `src\index.css` (complete theme)

**Icons:**
- `lucide-react` package

---

## Integration Steps

### 1. Copy Component Files

```bash
# From admin_panel_test/client/src
cp pages/DashboardClient.tsx → client_copier/gui/src/pages/dashboards/
cp components/DashboardLayout.tsx → client_copier/gui/src/components/
cp index.css → client_copier/gui/src/
```

### 2. Install Dependencies

```bash
cd client_copier/gui
npm install lucide-react sonner wouter
```

### 3. Update Imports

In `DashboardClient.tsx`, change:

```tsx
// FROM:
import { useMockAuth } from "@/contexts/MockAuthContext";

// TO:
import { useAuth } from "@/contexts/AuthContext"; // Your real auth
```

### 4. Replace Mock Data

**Current (Mock):**
```tsx
const mockBalance = 50000.00;
const mockTrades = [...]; // Static array
```

**Replace with API calls:**
```tsx
const [balance, setBalance] = useState(0);
const [trades, setTrades] = useState([]);

useEffect(() => {
    loadDashboardData();
}, []);

const loadDashboardData = async () => {
    const data = await api.getDashboardData(token);
    setBalance(data.balance);
    setTrades(data.recentTrades);
};
```

### 5. Update Routing

In `client_copier/gui/src/App.tsx`:

```tsx
import DashboardClient from './pages/dashboards/DashboardClient';

<Route path="/dashboard">
  {isAuthenticated ? <DashboardClient /> : <Redirect to="/login" />}
</Route>
```

---

## API Integration Points

### Required API Endpoints

**1. Get Account Balance**
```typescript
GET /api/account/balance
Response: { balance: number, equity: number, margin: number }
```

**2. Get Recent Trades**
```typescript
GET /api/trades/recent?limit=10
Response: Trade[]

interface Trade {
    ticket: number;
    symbol: string;
    type: 'BUY' | 'SELL';
    volume: number;
    open_price: number;
    close_price?: number;
    profit: number;
    open_time: string;
    close_time?: string;
}
```

**3. Get Performance Metrics**
```typescript
GET /api/account/metrics
Response: {
    totalTrades: number;
    winRate: number;
    profitFactor: number;
}
```

---

## Component Structure

```tsx
export default function DashboardClient() {
    const { user } = useAuth(); // Replace MockAuth
    const [balance, setBalance] = useState(0);
    const [trades, setTrades] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        try {
            // API calls here
            const balanceData = await api.getBalance(token);
            const tradesData = await api.getRecentTrades(token);
            
            setBalance(balanceData.balance);
            setTrades(tradesData);
        } catch (error) {
            toast.error('Failed to load dashboard data');
        } finally {
            setLoading(false);
        }
    };

    return (
        <DashboardLayout role="CLIENT" username={user?.username}>
            {/* Dashboard content */}
        </DashboardLayout>
    );
}
```

---

## Styling

### Theme Variables

All theme variables are in `index.css`:

```css
:root {
  --primary: oklch(0.6 0.18 240); /* Electric Blue */
  --background: oklch(0.15 0.04 250); /* Deep Navy */
  /* ... more variables */
}
```

### Custom Classes

```css
.glass-panel { /* Glassmorphism card */ }
.text-glow { /* Glowing text */ }
.btn-gradient-primary { /* Primary button */ }
```

---

## Real-Time Updates (Future)

### WebSocket Integration

```tsx
useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/trades');
    
    ws.onmessage = (event) => {
        const trade = JSON.parse(event.data);
        setTrades(prev => [trade, ...prev].slice(0, 10));
    };

    return () => ws.close();
}, []);
```

---

## Differences from Test Version

| Feature | Test Version | Desktop Version |
|---------|-------------|-----------------|
| Auth | MockAuthContext | Real JWT tokens |
| Data | Static arrays | API calls |
| Updates | Manual refresh | WebSocket real-time |
| Storage | sessionStorage | Tauri store |
| Navigation | Wouter | Wouter (same) |

---

## Testing Checklist

After integration:

- [ ] Dashboard loads without errors
- [ ] Balance displays correctly
- [ ] Recent trades table populates
- [ ] Navigation works (sidebar links)
- [ ] Logout button functions
- [ ] Responsive on different screen sizes
- [ ] Theme/styling matches test version
- [ ] API calls succeed
- [ ] Error handling works (toast notifications)

---

## Contact Points

**Questions about:**
- **Styling/Theme:** Check `index.css` and `COMPONENTS.md`
- **Layout:** See `DashboardLayout.tsx`
- **Routing:** Refer to `App.tsx` in test version
- **API Integration:** See `services/api.ts` for structure

---

## Quick Reference

**Test Environment:**
```
admin_panel_test/client/
├── src/
│   ├── pages/DashboardClient.tsx ← MAIN FILE
│   ├── components/DashboardLayout.tsx ← LAYOUT
│   ├── index.css ← THEME
│   └── contexts/MockAuthContext.tsx ← REPLACE THIS
```

**Production Environment:**
```
client_copier/gui/
├── src/
│   ├── pages/dashboards/DashboardClient.tsx ← COPY HERE
│   ├── components/DashboardLayout.tsx ← COPY HERE
│   ├── index.css ← COPY HERE
│   └── contexts/AuthContext.tsx ← USE THIS
```

---

## Notes

- **Keep the styling exactly as is** - "Deep Ocean Glass" theme is complete
- **Replace only the data layer** - UI components work perfectly
- **Use the same component structure** - Just swap mock data for real API
- **Maintain responsive design** - Already mobile-friendly
- **Toast notifications are configured** - Colors are customized (green/red/yellow)
