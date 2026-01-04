import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { 
  ArrowUpRight, 
  ArrowDownRight, 
  DollarSign, 
  CreditCard, 
  Activity, 
  TrendingUp,
  MoreHorizontal
} from "lucide-react";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, BarChart, Bar, Cell } from "recharts";

const data = [
  { name: "Jan", total: 2400 },
  { name: "Fev", total: 1398 },
  { name: "Mar", total: 9800 },
  { name: "Abr", total: 3908 },
  { name: "Mai", total: 4800 },
  { name: "Jun", total: 3800 },
  { name: "Jul", total: 4300 },
];

const spendingData = [
  { name: "Aluguel", value: 35, color: "var(--chart-1)" },
  { name: "Serviços", value: 20, color: "var(--chart-2)" },
  { name: "Lazer", value: 15, color: "var(--chart-3)" },
  { name: "Invest.", value: 30, color: "var(--chart-4)" },
];

const transactions = [
  { id: 1, name: "Netflix Subscription", date: "Hoje, 10:00", amount: "-$15.00", status: "completed", icon: "🎬" },
  { id: 2, name: "Apple Store", date: "Ontem, 14:30", amount: "-$240.00", status: "completed", icon: "🍎" },
  { id: 3, name: "Freelance Payment", date: "22 Jan, 09:00", amount: "+$1,250.00", status: "income", icon: "💼" },
  { id: 4, name: "Spotify Premium", date: "20 Jan, 11:00", amount: "-$12.00", status: "completed", icon: "🎵" },
];

export default function Home() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-display font-bold text-white tracking-tight text-glow">
              Visão Geral
            </h1>
            <p className="text-muted-foreground mt-1">
              Bem-vindo de volta, aqui está o resumo financeiro de hoje.
            </p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="bg-white/5 border-white/10 hover:bg-white/10 text-white backdrop-blur-md">
              Download Relatório
            </Button>
            <Button className="bg-gradient-to-r from-primary to-cyan-500 hover:opacity-90 text-white border-0 shadow-lg shadow-primary/25">
              Nova Transação
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {[
            { title: "Saldo Total", value: "$45,231.89", change: "+20.1%", trend: "up", icon: DollarSign, color: "text-cyan-400" },
            { title: "Receita", value: "$8,340.00", change: "+12.5%", trend: "up", icon: TrendingUp, color: "text-emerald-400" },
            { title: "Despesas", value: "$2,420.50", change: "-4.3%", trend: "down", icon: CreditCard, color: "text-rose-400" },
            { title: "Investimentos", value: "$12,890.00", change: "+8.2%", trend: "up", icon: Activity, color: "text-violet-400" },
          ].map((stat, i) => (
            <Card key={i} className="glass-panel border-0 relative overflow-hidden group hover:-translate-y-1 transition-all duration-300">
              <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {stat.title}
                </CardTitle>
                <div className={`p-2 rounded-lg bg-white/5 ${stat.color}`}>
                  <stat.icon className="h-4 w-4" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white font-display tracking-tight">{stat.value}</div>
                <div className="flex items-center text-xs mt-1">
                  {stat.trend === "up" ? (
                    <ArrowUpRight className="mr-1 h-4 w-4 text-emerald-400" />
                  ) : (
                    <ArrowDownRight className="mr-1 h-4 w-4 text-rose-400" />
                  )}
                  <span className={stat.trend === "up" ? "text-emerald-400" : "text-rose-400"}>
                    {stat.change}
                  </span>
                  <span className="text-muted-foreground ml-1">vs mês anterior</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Charts Section */}
        <div className="grid gap-6 md:grid-cols-7">
          {/* Revenue Chart */}
          <Card className="col-span-4 glass-panel border-0">
            <CardHeader>
              <CardTitle className="text-white font-display">Fluxo de Caixa</CardTitle>
            </CardHeader>
            <CardContent className="pl-2">
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data}>
                    <defs>
                      <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="var(--primary)" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <XAxis 
                      dataKey="name" 
                      stroke="#888888" 
                      fontSize={12} 
                      tickLine={false} 
                      axisLine={false} 
                    />
                    <YAxis 
                      stroke="#888888" 
                      fontSize={12} 
                      tickLine={false} 
                      axisLine={false} 
                      tickFormatter={(value) => `$${value}`} 
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '12px',
                        color: '#fff'
                      }} 
                    />
                    <Area 
                      type="monotone" 
                      dataKey="total" 
                      stroke="var(--primary)" 
                      strokeWidth={3}
                      fillOpacity={1} 
                      fill="url(#colorTotal)" 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          {/* Spending Categories */}
          <Card className="col-span-3 glass-panel border-0">
            <CardHeader>
              <CardTitle className="text-white font-display">Gastos por Categoria</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={spendingData} layout="vertical" margin={{ left: 0, right: 0 }}>
                    <XAxis type="number" hide />
                    <YAxis 
                      dataKey="name" 
                      type="category" 
                      stroke="#888888" 
                      fontSize={12} 
                      tickLine={false} 
                      axisLine={false} 
                      width={60}
                    />
                    <Tooltip
                      cursor={{fill: 'transparent'}}
                      contentStyle={{ 
                        backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '12px',
                        color: '#fff'
                      }}
                    />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={32}>
                      {spendingData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Transactions & Quick Transfer */}
        <div className="grid gap-6 md:grid-cols-3">
          <Card className="col-span-2 glass-panel border-0">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="text-white font-display">Transações Recentes</CardTitle>
              <Button variant="ghost" size="sm" className="text-cyan-400 hover:text-cyan-300 hover:bg-cyan-400/10">
                Ver tudo
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {transactions.map((transaction) => (
                  <div key={transaction.id} className="flex items-center justify-between group cursor-pointer">
                    <div className="flex items-center gap-4">
                      <div className="h-10 w-10 rounded-full bg-white/5 flex items-center justify-center text-lg group-hover:bg-primary/20 transition-colors">
                        {transaction.icon}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-white group-hover:text-cyan-300 transition-colors">
                          {transaction.name}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {transaction.date}
                        </p>
                      </div>
                    </div>
                    <div className={`text-sm font-bold ${transaction.status === 'income' ? 'text-emerald-400' : 'text-white'}`}>
                      {transaction.amount}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="col-span-1 glass-panel border-0 bg-gradient-to-b from-primary/20 to-transparent">
            <CardHeader>
              <CardTitle className="text-white font-display">Cartão Virtual</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="relative h-48 w-full rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-700 p-6 shadow-2xl shadow-cyan-500/20 overflow-hidden group">
                <div className="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-white/10 blur-3xl group-hover:bg-white/20 transition-all" />
                <div className="relative z-10 flex flex-col justify-between h-full">
                  <div className="flex justify-between items-start">
                    <span className="font-display font-bold text-white text-lg italic">VISA</span>
                    <Activity className="h-6 w-6 text-white/80" />
                  </div>
                  <div>
                    <p className="text-white/80 text-sm mb-1">Balance</p>
                    <p className="text-white font-bold text-2xl tracking-tight">$12,450.00</p>
                  </div>
                  <div className="flex justify-between items-end">
                    <p className="text-white/90 font-mono text-sm">**** **** **** 4289</p>
                    <p className="text-white/80 text-xs">12/25</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Limite Diário</span>
                  <span className="text-white font-medium">$5,000</span>
                </div>
                <div className="h-2 w-full bg-white/10 rounded-full overflow-hidden">
                  <div className="h-full w-[65%] bg-gradient-to-r from-cyan-400 to-primary rounded-full" />
                </div>
                <p className="text-xs text-muted-foreground text-right">65% utilizado</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
