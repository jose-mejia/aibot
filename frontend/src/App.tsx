import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import { apiService } from './services/api';

function App() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const data = await apiService.getStatus();
      setStatus(data);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao buscar status:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="app-loading">
        <div className="spinner"></div>
        <p>Carregando sistema...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>🤖 AI Trading Bot</h1>
        <p>Sistema de Trading Automatizado com MetaTrader 5</p>
      </header>
      <Dashboard status={status} onStatusChange={fetchStatus} />
    </div>
  );
}

export default App;
