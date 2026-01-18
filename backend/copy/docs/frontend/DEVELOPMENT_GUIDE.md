# Frontend Development Guide

## Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
cd admin_panel_test/client
npm install
```

### Development Server

```bash
npm run dev
```

Access at: `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Output: `dist/`

---

## Creating New Pages

### 1. Create Page Component

**Location:** `src/pages/YourPage.tsx`

```tsx
import DashboardLayout from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";

export default function YourPage() {
    const { user } = useAuth();

    return (
        <DashboardLayout role={user?.role as any} username={user?.username}>
            <div className="space-y-6 animate-fade-in pb-10">
                <div>
                    <h2 className="text-3xl font-bold font-display text-white mb-1 text-glow">
                        Page Title
                    </h2>
                    <p className="text-muted-foreground">Page description</p>
                </div>

                {/* Your content here */}
            </div>
        </DashboardLayout>
    );
}
```

### 2. Register Route

**Location:** `src/App.tsx`

```tsx
import YourPage from "./pages/YourPage";

// Add route
<Route path="/your-route">
  {isAuthenticated ? <YourPage /> : <Redirect to="/login" />}
</Route>
```

### 3. Add to Navigation

**Location:** `src/components/DashboardLayout.tsx`

```tsx
const adminNavigation = [
  // ... existing items
  { name: "Your Page", href: "/your-route", icon: YourIcon },
];
```

---

## Adding New Features

### Modal Dialog

```tsx
const [isModalOpen, setIsModalOpen] = useState(false);

// Modal JSX
{isModalOpen && (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-in fade-in">
        <div className="glass-panel p-6 rounded-2xl border border-white/10 max-w-md w-full mx-4">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white">Modal Title</h3>
                <button onClick={() => setIsModalOpen(false)}>
                    <X className="h-5 w-5" />
                </button>
            </div>
            {/* Modal content */}
        </div>
    </div>
)}
```

### Data Table

```tsx
<div className="glass-panel rounded-2xl overflow-hidden border border-white/5">
    <div className="overflow-x-auto">
        <table className="w-full text-left">
            <thead className="bg-black/20 text-xs uppercase text-muted-foreground">
                <tr>
                    <th className="px-6 py-4">Column 1</th>
                    <th className="px-6 py-4">Column 2</th>
                </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
                {data.map(item => (
                    <tr key={item.id} className="hover:bg-white/5 transition-colors">
                        <td className="px-6 py-4">{item.field1}</td>
                        <td className="px-6 py-4">{item.field2}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
</div>
```

### Form Input

```tsx
<div className="space-y-2">
    <label className="text-xs font-bold text-muted-foreground uppercase">
        Field Label
    </label>
    <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-primary/50"
        placeholder="Enter value..."
    />
</div>
```

### Select Dropdown

```tsx
<select 
    value={selected}
    onChange={(e) => setSelected(e.target.value)}
    className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:border-primary/50"
>
    <option value="option1">Option 1</option>
    <option value="option2">Option 2</option>
</select>
```

### Search Bar

```tsx
const [searchTerm, setSearchTerm] = useState('');

<div className="relative">
    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
    <input
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="pl-9 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm text-white focus:outline-none focus:border-primary/50"
    />
</div>
```

---

## Styling Guide

### Color Usage

**Primary Actions:**
```tsx
<button className="btn-gradient-primary px-6 py-3 rounded-lg">
  Primary Action
</button>
```

**Secondary Actions:**
```tsx
<button className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10">
  Secondary Action
</button>
```

**Destructive Actions:**
```tsx
<button className="px-4 py-2 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg hover:bg-red-500/20">
  Delete
</button>
```

### Status Badges

```tsx
// Success
<span className="px-2 py-0.5 rounded text-[10px] font-bold bg-green-500/20 text-green-400">
  Active
</span>

// Warning
<span className="px-2 py-0.5 rounded text-[10px] font-bold bg-yellow-500/20 text-yellow-400">
  Pending
</span>

// Error
<span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400">
  Inactive
</span>
```

### Card Layouts

```tsx
<div className="glass-panel p-6 rounded-2xl border border-white/5">
    <div className="flex items-center gap-3 mb-6 border-b border-white/5 pb-4">
        <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
            <Icon className="h-5 w-5 text-primary" />
        </div>
        <div>
            <h3 className="text-lg font-bold text-white">Card Title</h3>
            <p className="text-xs text-muted-foreground">Card subtitle</p>
        </div>
    </div>
    {/* Card content */}
</div>
```

---

## State Management Patterns

### Local State

```tsx
const [data, setData] = useState<DataType[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
```

### Form State

```tsx
interface FormData {
    field1: string;
    field2: string;
}

const [formData, setFormData] = useState<FormData>({
    field1: '',
    field2: '',
});

const handleChange = (field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
};
```

### Search/Filter State

```tsx
const [searchTerm, setSearchTerm] = useState('');
const [filter, setFilter] = useState<'all' | 'active' | 'inactive'>('all');

const filteredData = data.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || item.status === filter;
    return matchesSearch && matchesFilter;
});
```

---

## API Integration (Future)

### Mock API Service

**Location:** `src/services/api.ts`

Currently returns static data. To integrate real API:

```tsx
// Replace mock implementation
export const api = {
    async getUsers(token: string) {
        const response = await fetch('/api/users', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        return response.json();
    },
    
    async updateUser(token: string, userId: number, data: UserData) {
        const response = await fetch(`/api/users/${userId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return response.json();
    }
};
```

---

## Testing

### Manual Testing Checklist

**Login Flow:**
- [ ] Can login as Client
- [ ] Can login as Master
- [ ] Can login as Admin
- [ ] Redirects to correct dashboard

**Navigation:**
- [ ] All sidebar links work
- [ ] Active route is highlighted
- [ ] Mobile menu works
- [ ] Logout button visible and functional

**Admin Features:**
- [ ] Can search users in Accounts
- [ ] Can edit user details
- [ ] Modal opens/closes correctly
- [ ] Changes are saved (mock)
- [ ] Toast notifications appear

**Responsive Design:**
- [ ] Works on desktop (1920x1080)
- [ ] Works on tablet (768x1024)
- [ ] Works on mobile (375x667)
- [ ] Sidebar collapses on mobile

---

## Troubleshooting

### Build Errors

**Error:** Module not found
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error:** TypeScript errors
```bash
# Check tsconfig.json
# Ensure all imports use correct paths (@/ alias)
```

### Runtime Errors

**Error:** White screen
- Check browser console for errors
- Verify all routes are registered
- Check ErrorBoundary is wrapping App

**Error:** Styles not applying
- Verify Tailwind is configured
- Check `index.css` is imported in `main.tsx`
- Clear browser cache

### Development Tips

**Hot Reload Not Working:**
```bash
# Restart dev server
npm run dev
```

**Port Already in Use:**
```bash
# Change port in vite.config.ts
server: {
  port: 5174
}
```

---

## Performance Optimization

### Code Splitting

```tsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

<Suspense fallback={<div>Loading...</div>}>
  <HeavyComponent />
</Suspense>
```

### Memoization

```tsx
import { useMemo } from 'react';

const expensiveValue = useMemo(() => {
    return computeExpensiveValue(data);
}, [data]);
```

---

## Deployment

### Build

```bash
npm run build
```

### Preview Build

```bash
npm run preview
```

### Deploy to Static Hosting

```bash
# Upload dist/ folder to:
# - Vercel
# - Netlify
# - GitHub Pages
# - AWS S3
```

---

## Next Steps

1. **Backend Integration:** Replace mock API with real endpoints
2. **WebSocket:** Add real-time signal updates
3. **Authentication:** Implement JWT tokens
4. **Database:** Connect to PostgreSQL
5. **Desktop App:** Migrate to Tauri
