import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import ControlPanel from './ControlPanel';
import ConfigPanel from './ConfigPanel';
import OperationsPanel from './OperationsPanel';
import LogsPanel from './LogsPanel';
import AssetsPanel from './AssetsPanel';
import { apiService } from '../services/api';

interface DashboardProps {
  status: any;
  onStatusChange: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ status, onStatusChange }) => {
  const [activeTab, setActiveTab] = useState<'control' | 'config' | 'operations' | 'logs' | 'assets'>('control');
  const [trades, setTrades] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);

  useEffect(() => {
    if (status?.bot_running) {
      const interval = setInterval(() => {
        fetchData();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [status?.bot_running]);

  const fetchData = async () => {
    try {
      const [tradesData, logsData] = await Promise.all([
        apiService.getTrades(50),
        apiService.getLogs(100),
      ]);
      setTrades(tradesData);
      setLogs(logsData);
    } catch (error) {
      console.error('Erro ao buscar dados:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-tabs">
        <button
          className={activeTab === 'control' ? 'active' : ''}
          onClick={() => setActiveTab('control')}
        >
          🎮 Controle
        </button>
        <button
          className={activeTab === 'config' ? 'active' : ''}
          onClick={() => setActiveTab('config')}
        >
          ⚙️ Configurações
        </button>
        <button
          className={activeTab === 'operations' ? 'active' : ''}
          onClick={() => setActiveTab('operations')}
        >
          📈 Operações
        </button>
        <button
          className={activeTab === 'logs' ? 'active' : ''}
          onClick={() => setActiveTab('logs')}
        >
          📝 Logs
        </button>
        <button
          className={activeTab === 'assets' ? 'active' : ''}
          onClick={() => setActiveTab('assets')}
        >
          📊 Ativos
        </button>
      </div>

      <div className="dashboard-content">
        {activeTab === 'control' && (
          <ControlPanel status={status} onStatusChange={onStatusChange} />
        )}
        {activeTab === 'config' && (
          <ConfigPanel onConfigChange={onStatusChange} />
        )}
        {activeTab === 'operations' && (
          <OperationsPanel trades={trades} />
        )}
        {activeTab === 'logs' && (
          <LogsPanel logs={logs} />
        )}
        {activeTab === 'assets' && (
          <AssetsPanel />
        )}
      </div>
    </div>
  );
};

export default Dashboard;
