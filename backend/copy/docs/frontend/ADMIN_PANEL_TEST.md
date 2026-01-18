> [!IMPORTANT]
> **Status: ARCHIVED / PROTOTYPE**  
> This documentation refers to the static prototype used for UI validation. The production-ready integrated version is located in `api_server/admin_panel`. For current development, please refer to [STRUCTURE.md](./STRUCTURE.md) and [DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md).

## Overview

The `admin_panel_test` was the static, fully-featured frontend prototype.

**Location:** `C:\Users\josemejia\dev\python\aibot\backend\copy\admin_panel_test\client`

## Architecture

### Tech Stack

- **Framework:** React 18 + TypeScript
- **Routing:** Wouter (lightweight React router)
- **Styling:** Tailwind CSS with custom theme
- **UI Components:** shadcn/ui
- **Notifications:** Sonner (toast notifications)
- **Build Tool:** Vite
- **State Management:** React Context API (MockAuthContext)

### Project Structure

```
admin_panel_test/client/
├── src/
│   ├── components/
│   │   ├── DashboardLayout.tsx    # Main layout with sidebar
│   │   ├── ErrorBoundary.tsx      # Error handling
│   │   └── ui/                    # shadcn/ui components
│   ├── contexts/
│   │   ├── MockAuthContext.tsx    # Authentication simulation
│   │   └── ThemeContext.tsx       # Theme management
│   ├── pages/
│   │   ├── admin/                 # Admin-specific pages
│   │   │   ├── Accounts.tsx       # User management with edit modal
│   │   │   ├── RegisterUser.tsx   # User registration form
│   │   │   ├── MT5Connection.tsx  # Admin MT5 connections
│   │   │   ├── MT5Status.tsx      # MT5 account status
│   │   │   ├── APIDocs.tsx        # API documentation
│   │   │   ├── AuditLogs.tsx      # System audit logs
│   │   │   ├── Settings.tsx       # Settings placeholder
│   │   │   ├── SystemStatus.tsx   # System status
│   │   │   ├── UserManagement.tsx # User management
│   │   │   └── ServerConfig.tsx   # Server configuration
│   │   ├── DashboardClient.tsx    # Client dashboard
│   │   ├── DashboardMaster.tsx    # Master dashboard
│   │   ├── DashboardAdmin.tsx     # Admin dashboard
│   │   ├── LoginMockup.tsx        # Login page with role selection
│   │   ├── MT5ConnectionPage.tsx  # Client/Master MT5 config
│   │   ├── TradingConfigPage.tsx  # Master trading config
│   │   ├── Profile.tsx            # User profile
│   │   ├── SignalMonitor.tsx      # Signal monitoring
│   │   └── NotFound.tsx           # 404 page
│   ├── services/
│   │   └── api.ts                 # Mock API service
│   ├── App.tsx                    # Main app with routing
│   ├── index.css                  # Global styles + theme
│   └── main.tsx                   # Entry point
└── package.json
```

## Design System

### Theme: "Deep Ocean Glass"

The design follows a glassmorphism aesthetic with deep ocean blue tones:

**Color Palette:**
- **Primary:** Electric Blue (`oklch(0.6 0.18 240)`)
- **Background:** Deep Navy (`oklch(0.15 0.04 250)`)
- **Foreground:** Ice White (`oklch(0.95 0.02 240)`)
- **Glass Cards:** Semi-transparent Navy with backdrop blur

**Key Visual Elements:**
- Glassmorphism panels with `backdrop-blur-xl`
- Subtle borders (`border-white/10`)
- Text glow effects on headings
- Smooth animations and transitions
- Custom scrollbar styling

### Toast Notifications

Custom colored toast notifications for better UX:

- **Success:** Green (`oklch(0.25 0.15 145)`)
- **Error:** Red (`oklch(0.25 0.15 20)`)
- **Warning:** Yellow (`oklch(0.25 0.15 60)`)
- **Info:** Blue (`oklch(0.25 0.15 240)`)

## Routing System

### Route Namespacing

To prevent conflicts between roles, all routes are namespaced:

**Client Routes** (`/client/*`):
- `/dashboard-client` - Client dashboard
- `/client/signals` - Signal monitor
- `/client/mt5-connection` - MT5 configuration
- `/client/settings` - Settings
- `/client/profile` - User profile

**Master Routes** (`/master/*`):
- `/dashboard-master` - Master dashboard
- `/master/signals` - Signal monitor
- `/master/mt5-connection` - MT5 configuration
- `/master/trading-config` - Trading configuration
- `/master/settings` - Settings
- `/master/profile` - User profile

**Admin Routes** (`/admin/*`):
- `/dashboard-admin` - Admin dashboard
- `/admin/accounts` - User accounts (with edit modal)
- `/admin/register-user` - User registration
- `/admin/signals` - Signal monitor
- `/admin/mt5-connection` - MT5 connections
- `/admin/mt5-status` - MT5 status
- `/admin/api-docs` - API documentation
- `/admin/audit-logs` - Audit logs
- `/admin/profile` - User profile
- `/admin/settings` - Settings

### Backward Compatibility

Legacy routes redirect to the appropriate namespaced route based on user role:
- `/settings` → `/client/settings` | `/master/settings` | `/admin/settings`
- `/profile` → `/client/profile` | `/master/profile` | `/admin/profile`

## Authentication

### MockAuthContext

Simulates authentication without a backend:

```typescript
interface User {
  username: string;
  role: 'CLIENT' | 'MASTER' | 'ADMIN';
}

// Available mock users:
- client_demo (CLIENT)
- master_sender (MASTER)
- admin (ADMIN)
```

**Features:**
- Login with role selection
- Logout functionality
- Session persistence (sessionStorage)
- Protected routes

## Key Components

### DashboardLayout

Main layout component with role-based navigation:

**Features:**
- Dynamic sidebar based on user role
- Always-visible logout button (fixed at bottom)
- Mobile-responsive menu
- Search bar in header
- User avatar and role display

**Navigation Arrays:**
- `clientNavigation` - 5 items
- `masterNavigation` - 6 items
- `adminNavigation` - 10 items

### Accounts Page (Admin)

Most important admin page with full CRUD functionality:

**Features:**
- Search/filter users
- Click-to-edit modal
- Editable fields:
  - Username
  - Role (CLIENT/MASTER/ADMIN)
  - Phone
  - MT5 ID
  - Status (Active/Inactive/Suspended)
- Password field excluded (as requested)
- Toast notifications on save

## Static Data

All pages use mock/static data for demonstration:

**Mock Data Sources:**
- User accounts (3 users)
- MT5 connections
- Signals/trades
- System status
- Audit logs

## Running the Application

### Development

```bash
cd admin_panel_test/client
npm install
npm run dev
```

Access at: `http://localhost:5173`

### Login

1. Navigate to `/login`
2. Select a role:
   - **Client** → `client_demo`
   - **Master** → `master_sender`
   - **Admin** → `admin`
3. Click "Login" (no password required in mock mode)

### Testing Different Roles

1. **Client:** Limited access (Dashboard, Signals, MT5 Connection, Settings, Profile)
2. **Master:** Extended access (+ Trading Config)
3. **Admin:** Full access (10 menu items including user management)

## Styling Guidelines

### CSS Classes

**Utility Classes:**
- `.glass-panel` - Glassmorphism card
- `.glass-card-hover` - Hover effects for cards
- `.text-glow` - Text glow effect
- `.btn-gradient-primary` - Primary gradient button
- `.input-field` - Standard input styling

**Spacing:**
- All pages use `pb-10` for bottom padding
- Consistent `space-y-6` for vertical spacing
- `animate-fade-in` for page transitions

## Future Enhancements

### Phase 3: Migration to Desktop (Planned)

- Tauri integration for desktop app
- Real API integration
- WebSocket for real-time updates
- Database persistence

## Troubleshooting

### Common Issues

**Issue:** Routes not working
- **Solution:** Check route namespacing in `App.tsx`

**Issue:** Sidebar not showing correct items
- **Solution:** Verify `role` prop is passed to `DashboardLayout`

**Issue:** Toast notifications not appearing
- **Solution:** Ensure `<Toaster />` is in `App.tsx`

**Issue:** Logout button not visible
- **Solution:** Check sidebar has `shrink-0` on logout container

## File Locations

**Main Files:**
- Layout: `src/components/DashboardLayout.tsx`
- Routing: `src/App.tsx`
- Styles: `src/index.css`
- Auth: `src/contexts/MockAuthContext.tsx`

**Admin Pages:**
- `src/pages/admin/Accounts.tsx` (most important)
- `src/pages/admin/RegisterUser.tsx`
- `src/pages/admin/MT5Status.tsx`
- `src/pages/admin/APIDocs.tsx`
- `src/pages/admin/AuditLogs.tsx`

## Notes

- All data is **static/mock** - no backend required
- Designed for **demonstration and testing**
- Follows **Deep Ocean Glass** aesthetic strictly
- **Fully responsive** (desktop + mobile)
- **Role-based access control** via routing
