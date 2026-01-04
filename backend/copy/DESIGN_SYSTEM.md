# 🎨 AIBOT Trade Copier - Design System

## Paleta de Cores

### Cores Principais
```css
--primary-bg: #0A0E27;           /* Fundo principal escuro */
--secondary-bg: #131829;         /* Fundo cards/sidebar */
--card-bg: #1A1F3A;              /* Fundo cards elevados */

--primary-blue: #00D9FF;         /* Cyan brilhante */
--secondary-blue: #2E5BFF;       /* Azul royal */
--accent-purple: #8B5CF6;        /* Roxo accent */

--success: #10B981;              /* Verde sucesso */
--warning: #F59E0B;              /* Amarelo warning */
--error: #EF4444;                /* Vermelho erro */
--info: #3B82F6;                 /* Azul info */

--text-primary: #FFFFFF;         /* Texto principal */
--text-secondary: #94A3B8;       /* Texto secundário */
--text-muted: #64748B;           /* Texto desativado */

--border-color: rgba(255, 255, 255, 0.1);
--hover-bg: rgba(0, 217, 255, 0.1);
```

### Gradientes
```css
--gradient-primary: linear-gradient(135deg, #2E5BFF 0%, #00D9FF 100%);
--gradient-card: linear-gradient(135deg, rgba(46, 91, 255, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%);
--gradient-success: linear-gradient(135deg, #10B981 0%, #34D399 100%);
--gradient-error: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
```

---

## Tipografia

### Fontes
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Tamanhos
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 2rem;      /* 32px */
```

### Pesos
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

---

## Componentes

### 1. Botões

#### Primário (Ação principal)
```css
background: linear-gradient(135deg, #2E5BFF 0%, #00D9FF 100%);
color: white;
padding: 12px 24px;
border-radius: 8px;
font-weight: 600;
box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
transition: all 0.3s ease;

/* Hover */
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(0, 217, 255, 0.4);
```

#### Secundário
```css
background: rgba(255, 255, 255, 0.05);
border: 1px solid rgba(255, 255, 255, 0.1);
color: #94A3B8;
```

#### Sucesso
```css
background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
```

#### Perigo
```css
background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
```

---

### 2. Cards

```css
background: #1A1F3A;
border-radius: 16px;
padding: 24px;
border: 1px solid rgba(255, 255, 255, 0.05);
box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
backdrop-filter: blur(10px);
transition: all 0.3s ease;

/* Hover */
border-color: rgba(0, 217, 255, 0.2);
transform: translateY(-4px);
box-shadow: 0 8px 32px rgba(0, 217, 255, 0.15);
```

---

### 3. Inputs

```css
background: rgba(255, 255, 255, 0.05);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 8px;
padding: 12px 16px;
color: white;
font-size: 14px;
transition: all 0.3s ease;

/* Focus */
border-color: #00D9FF;
box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.1);
background: rgba(255, 255, 255, 0.08);
```

---

### 4. Badges/Status

#### Conectado
```css
background: rgba(16, 185, 129, 0.15);
color: #10B981;
border: 1px solid rgba(16, 185, 129, 0.3);
padding: 4px 12px;
border-radius: 12px;
font-size: 12px;
font-weight: 600;
```

#### Desconectado
```css
background: rgba(239, 68, 68, 0.15);
color: #EF4444;
border: 1px solid rgba(239, 68, 68, 0.3);
```

#### Processando
```css
background: rgba(245, 158, 11, 0.15);
color: #F59E0B;
border: 1px solid rgba(245, 158, 11, 0.3);
```

---

### 5. Tabelas

```css
/* Header */
background: rgba(255, 255, 255, 0.03);
color: #94A3B8;
font-weight: 600;
font-size: 12px;
text-transform: uppercase;
letter-spacing: 0.05em;
padding: 12px 16px;

/* Rows */
border-bottom: 1px solid rgba(255, 255, 255, 0.05);
padding: 16px;
transition: background 0.2s ease;

/* Hover */
background: rgba(0, 217, 255, 0.05);
```

---

### 6. Sidebar/Menu

```css
background: #131829;
width: 240px;
border-right: 1px solid rgba(255, 255, 255, 0.05);

/* Menu Item */
padding: 12px 20px;
color: #94A3B8;
border-radius: 8px;
margin: 4px 12px;
transition: all 0.2s ease;

/* Active */
background: linear-gradient(135deg, rgba(46, 91, 255, 0.15) 0%, rgba(0, 217, 255, 0.1) 100%);
color: #00D9FF;
border-left: 3px solid #00D9FF;
```

---

### 7. Gráficos

```css
/* Linha principal */
stroke: url(#gradient-primary);
stroke-width: 2px;
fill: none;

/* Área sob a curva */
fill: url(#gradient-area);
opacity: 0.3;

/* Grid */
stroke: rgba(255, 255, 255, 0.05);
stroke-dasharray: 4 4;
```

---

### 8. Modais

```css
background: #1A1F3A;
border-radius: 16px;
padding: 32px;
border: 1px solid rgba(255, 255, 255, 0.1);
box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
backdrop-filter: blur(20px);
max-width: 500px;

/* Overlay */
background: rgba(10, 14, 39, 0.8);
backdrop-filter: blur(8px);
```

---

### 9. Tooltips

```css
background: #1A1F3A;
color: white;
padding: 8px 12px;
border-radius: 6px;
font-size: 12px;
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
border: 1px solid rgba(255, 255, 255, 0.1);
```

---

### 10. Progress Bars

```css
background: rgba(255, 255, 255, 0.05);
height: 8px;
border-radius: 4px;
overflow: hidden;

/* Fill */
background: linear-gradient(90deg, #2E5BFF 0%, #00D9FF 100%);
height: 100%;
border-radius: 4px;
transition: width 0.3s ease;
box-shadow: 0 0 12px rgba(0, 217, 255, 0.5);
```

---

## Animações

### Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
animation: fadeIn 0.3s ease;
```

### Pulse (Loading)
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
animation: pulse 2s ease-in-out infinite;
```

### Slide In
```css
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}
```

### Glow
```css
@keyframes glow {
  0%, 100% { box-shadow: 0 0 20px rgba(0, 217, 255, 0.3); }
  50% { box-shadow: 0 0 40px rgba(0, 217, 255, 0.6); }
}
```

---

## Espaçamento

```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-2xl: 48px;
```

---

## Breakpoints (Responsivo)

```css
--mobile: 640px;
--tablet: 768px;
--desktop: 1024px;
--wide: 1280px;
```

---

## Ícones

Usar **Lucide Icons** ou **Heroicons** para consistência:
- Tamanho padrão: 20px
- Cor: Herdar do texto ou usar `--primary-blue`
- Stroke width: 2px

---

## Aplicação nos Componentes

### Admin Panel (React)
- Dashboard com cards de estatísticas
- Tabela de usuários/sinais
- Gráficos de performance
- Formulários de configuração

### Master Sender GUI (Desktop)
- Status de conexão MT5
- Lista de ordens enviadas
- Logs em tempo real
- Botão "Start/Stop"

### Client Copier GUI (Desktop)
- Status de conexão (MT5 + WebSocket)
- Ordens copiadas
- Safety rules status
- Performance metrics

---

## Exemplo de Implementação

### Card de Estatística
```html
<div class="stat-card">
  <div class="stat-icon">
    <svg><!-- ícone --></svg>
  </div>
  <div class="stat-content">
    <p class="stat-label">Saldo Total</p>
    <h3 class="stat-value">$45,231.89</h3>
    <span class="stat-change positive">+23.1% vs mês anterior</span>
  </div>
</div>
```

```css
.stat-card {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  gap: 16px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  border-color: rgba(0, 217, 255, 0.2);
  transform: translateY(-4px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, rgba(46, 91, 255, 0.2) 0%, rgba(0, 217, 255, 0.1) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin: 8px 0;
}

.stat-change.positive {
  color: var(--success);
}
```

---

## Próximos Passos

1. ✅ Criar arquivo CSS global (`design-system.css`)
2. ✅ Atualizar Admin Panel com novo design
3. ✅ Atualizar Master Sender GUI
4. ✅ Atualizar Client Copier GUI
5. ✅ Adicionar animações e transições
6. ✅ Testar responsividade

---

**Este design system garante consistência visual em todos os componentes do AIBOT Trade Copier!** 🎨
