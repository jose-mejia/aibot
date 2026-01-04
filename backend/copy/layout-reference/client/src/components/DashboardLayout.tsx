import { Link, useLocation } from "wouter";
import { cn } from "@/lib/utils";
import { 
  LayoutDashboard, 
  PieChart, 
  Wallet, 
  ArrowRightLeft, 
  Settings, 
  Bell, 
  Search,
  Menu,
  X
} from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [location] = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigation = [
    { name: "Visão Geral", href: "/", icon: LayoutDashboard },
    { name: "Análises", href: "/analytics", icon: PieChart },
    { name: "Transações", href: "/transactions", icon: ArrowRightLeft },
    { name: "Carteira", href: "/wallet", icon: Wallet },
    { name: "Configurações", href: "/settings", icon: Settings },
  ];

  return (
    <div className="min-h-screen flex bg-background/80 backdrop-blur-sm">
      {/* Sidebar Desktop */}
      <aside className="hidden md:flex w-64 flex-col fixed inset-y-0 z-50 glass-panel border-r border-white/10">
        <div className="p-6 flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary to-cyan-400 flex items-center justify-center shadow-lg shadow-primary/20">
            <Wallet className="h-6 w-6 text-white" />
          </div>
          <span className="font-display font-bold text-xl tracking-tight text-white">FinDash</span>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-2">
          {navigation.map((item) => {
            const isActive = location === item.href;
            return (
              <Link key={item.name} href={item.href}>
                <div
                  className={cn(
                    "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group cursor-pointer",
                    isActive
                      ? "bg-primary/20 text-white shadow-lg shadow-primary/10 border border-primary/20"
                      : "text-muted-foreground hover:text-white hover:bg-white/5"
                  )}
                >
                  <item.icon
                    className={cn(
                      "h-5 w-5 transition-colors",
                      isActive ? "text-cyan-400" : "text-muted-foreground group-hover:text-cyan-300"
                    )}
                  />
                  <span className="font-medium">{item.name}</span>
                  {isActive && (
                    <div className="ml-auto h-2 w-2 rounded-full bg-cyan-400 shadow-[0_0_10px_rgba(34,211,238,0.8)]" />
                  )}
                </div>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 mt-auto">
          <div className="glass-panel rounded-2xl p-4 bg-gradient-to-br from-primary/20 to-transparent border border-white/5">
            <div className="flex items-center gap-3 mb-3">
              <div className="h-8 w-8 rounded-full bg-white/10 flex items-center justify-center">
                <span className="text-xs font-bold text-cyan-300">PRO</span>
              </div>
              <div>
                <p className="text-sm font-bold text-white">Upgrade Plan</p>
                <p className="text-xs text-muted-foreground">Get more features</p>
              </div>
            </div>
            <Button size="sm" className="w-full bg-gradient-to-r from-primary to-cyan-500 hover:opacity-90 border-0">
              Upgrade Now
            </Button>
          </div>
        </div>
      </aside>

      {/* Mobile Header */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-50 glass-panel border-b border-white/10 px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-cyan-400 flex items-center justify-center">
            <Wallet className="h-5 w-5 text-white" />
          </div>
          <span className="font-display font-bold text-lg text-white">FinDash</span>
        </div>
        <Button variant="ghost" size="icon" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
          {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </Button>
      </div>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-40 bg-background/95 backdrop-blur-xl pt-20 px-6 md:hidden">
          <nav className="space-y-4">
            {navigation.map((item) => (
              <Link key={item.name} href={item.href}>
                <div
                  className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/10 text-white"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <item.icon className="h-6 w-6 text-cyan-400" />
                  <span className="text-lg font-medium">{item.name}</span>
                </div>
              </Link>
            ))}
          </nav>
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 md:pl-64 min-h-screen flex flex-col">
        {/* Topbar */}
        <header className="h-20 px-8 flex items-center justify-between sticky top-0 z-30 bg-background/50 backdrop-blur-md border-b border-white/5">
          <div className="hidden md:flex items-center gap-4 flex-1 max-w-md">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input 
                placeholder="Buscar transações, ativos..." 
                className="pl-10 bg-white/5 border-white/10 focus:bg-white/10 focus:border-primary/50 transition-all rounded-xl"
              />
            </div>
          </div>

          <div className="flex items-center gap-4 ml-auto">
            <Button variant="ghost" size="icon" className="relative text-muted-foreground hover:text-white hover:bg-white/5 rounded-xl">
              <Bell className="h-5 w-5" />
              <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-red-500 border-2 border-background" />
            </Button>
            
            <div className="flex items-center gap-3 pl-4 border-l border-white/10">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium text-white">Alex Morgan</p>
                <p className="text-xs text-muted-foreground">Premium User</p>
              </div>
              <Avatar className="h-10 w-10 border-2 border-primary/20">
                <AvatarImage src="https://github.com/shadcn.png" />
                <AvatarFallback>AM</AvatarFallback>
              </Avatar>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6 md:p-8 max-w-7xl mx-auto w-full animate-in fade-in slide-in-from-bottom-4 duration-700">
          {children}
        </div>
      </main>
    </div>
  );
}
