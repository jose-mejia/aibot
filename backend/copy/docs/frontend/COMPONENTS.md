# Frontend Components Reference

## Core Components

### DashboardLayout

**Location:** `src/components/DashboardLayout.tsx`

Main layout wrapper for all authenticated pages.

**Props:**
```typescript
interface DashboardLayoutProps {
  children: React.ReactNode;
  role?: "CLIENT" | "MASTER" | "ADMIN";
  username?: string;
}
```

**Features:**
- Role-based sidebar navigation
- Fixed logout button at bottom
- Mobile responsive menu
- Search bar in header
- User avatar display

**Usage:**
```tsx
<DashboardLayout role="ADMIN" username="admin">
  <YourPageContent />
</DashboardLayout>
```

---

### ErrorBoundary

**Location:** `src/components/ErrorBoundary.tsx`

Catches and displays React errors gracefully.

**Usage:**
```tsx
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

---

## Context Providers

### AuthContext

**Location:** `src/contexts/AuthContext.tsx`

Handles production-ready JWT authentication.

**API:**
```typescript
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  token: string | null;
}

const { user, isAuthenticated, login, logout } = useAuth();
```
---

### ThemeContext

**Location:** `src/contexts/ThemeContext.tsx`

Manages theme (always dark mode for "Deep Ocean Glass").

---

## Page Components

### Admin Pages

#### Accounts.tsx
**Most Important Admin Page**

Features:
- User list with search
- Click-to-edit modal
- Editable fields: username, role, phone, MT5 ID, status
- Toast notifications

```tsx
// State management
const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);
const [editForm, setEditForm] = useState<Account | null>(null);

// Open edit modal
handleEditClick(account);

// Save changes
handleSave();
```

#### RegisterUser.tsx
User registration form with role selection.

#### MT5Status.tsx
Displays MT5 account balances and status.

#### APIDocs.tsx
API endpoint documentation.

#### AuditLogs.tsx
System audit log viewer.

---

### Shared Pages

#### LoginMockup.tsx
Login page with role selection.

**Flow:**
1. User selects role
2. Clicks login
3. Redirected to appropriate dashboard

#### Profile.tsx
User profile editor (dynamic role detection).

#### SignalMonitor.tsx
Real-time signal monitoring (shared across roles).

#### MT5ConnectionPage.tsx
MT5 configuration (Client/Master).

**Props:**
```typescript
interface MT5ConnectionPageProps {
  role: 'CLIENT' | 'MASTER';
}
```

#### TradingConfigPage.tsx
Trading configuration (Master only).

---

## UI Components (shadcn/ui)

Located in `src/components/ui/`:

- `button.tsx` - Button component
- `input.tsx` - Input field
- `avatar.tsx` - User avatar
- `sonner.tsx` - Toast notifications
- `tooltip.tsx` - Tooltips

**Usage Example:**
```tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

<Button variant="ghost" size="icon">
  <Icon />
</Button>

<Input placeholder="Search..." />
```

---

## Styling Utilities

### Custom CSS Classes

**Glass Effects:**
```css
.glass-panel {
  /* Glassmorphism card with backdrop blur */
}

.glass-card-hover {
  /* Hover effects for interactive cards */
}
```

**Text Effects:**
```css
.text-glow {
  /* Glowing text effect for headings */
}
```

**Buttons:**
```css
.btn-gradient-primary {
  /* Primary gradient button */
}
```

**Inputs:**
```css
.input-field {
  /* Standard input styling */
}
```

### Tailwind Utilities

Common patterns:
```tsx
// Container with spacing
<div className="space-y-6 animate-fade-in pb-10">

// Glass panel
<div className="glass-panel p-6 rounded-2xl border border-white/5">

// Gradient button
<button className="btn-gradient-primary px-6 py-3 rounded-lg">

// Input field
<input className="input-field w-full px-4 py-3" />
```

---

## Toast Notifications

**Usage:**
```tsx
import { toast } from 'sonner';

// Success (green)
toast.success('User updated successfully');

// Error (red)
toast.error('Failed to save changes');

// Warning (yellow)
toast.warning('Please review your changes');

// Info (blue)
toast.info('Processing request...');
```

**Colors:**
- Success: Green background
- Error: Red background
- Warning: Yellow background
- Info: Blue background

---

## Routing Patterns

### Protected Routes

```tsx
<Route path="/admin/accounts">
  {isAuthenticated ? <Accounts /> : <Redirect to="/login" />}
</Route>
```

### Role-Based Redirects

```tsx
<Route path="/">
  {!isAuthenticated ? (
    <Redirect to="/login" />
  ) : (
    user?.role === "ADMIN" ? <Redirect to="/dashboard-admin" /> :
    user?.role === "MASTER" ? <Redirect to="/dashboard-master" /> :
    <Redirect to="/dashboard-client" />
  )}
</Route>
```

---

## Best Practices

### Best Practices

#### Component Structure

```tsx
import DashboardLayout from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";

export default function YourPage() {
    const { user } = useAuth();

    return (
        <DashboardLayout role={user?.role as any} username={user?.username}>
            <div className="space-y-6 animate-fade-in pb-10">
                {/* Your content */}
            </div>
        </DashboardLayout>
    );
}
```

### State Management

```tsx
// Local state for forms
const [formData, setFormData] = useState<FormType>({});

// Update field
setFormData({ ...formData, field: value });

// Submit
const handleSubmit = () => {
    // Validation
    if (!formData.field) {
        toast.error('Field is required');
        return;
    }
    
    // Save
    toast.success('Saved successfully');
};
```

### Modal Pattern

```tsx
const [isOpen, setIsOpen] = useState(false);
const [editData, setEditData] = useState<DataType | null>(null);

// Open modal
const handleEdit = (item: DataType) => {
    setEditData({ ...item });
    setIsOpen(true);
};

// Close modal
const handleClose = () => {
    setIsOpen(false);
    setEditData(null);
};

// Render modal
{isOpen && editData && (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
        <div className="glass-panel p-6 rounded-2xl max-w-md">
            {/* Modal content */}
        </div>
    </div>
)}
```

---

## Icons

Using `lucide-react`:

```tsx
import { 
  User, 
  Settings, 
  LogOut, 
  Edit, 
  Save,
  X 
} from 'lucide-react';

<User className="h-5 w-5 text-primary" />
```

Common icons:
- `LayoutDashboard` - Dashboard
- `Activity` - Signals/Status
- `Cable` - MT5 Connection
- `TrendingUp` - Trading
- `Settings` - Settings
- `User` - Profile/Users
- `Server` - Server/Config
- `LogOut` - Logout
- `Edit` - Edit
- `Save` - Save
- `X` - Close
