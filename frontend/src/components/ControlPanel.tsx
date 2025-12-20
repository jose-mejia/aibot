import React, { useState } from 'react';
import './ControlPanel.css';
import { apiService } from '../services/api';

interface ControlPanelProps {
  status: any;
  onStatusChange: () => void;
}

const ControlPanel: React.FC<ControlPanelProps> = ({ status, onStatusChange }) => {
  const [loading, setLoading] = useState(false);
  const [mt5Testing, setMt5Testing] = useState(false);

  const handleStart = async () => {
    setLoading(true);
    try {
      const result = await apiService.startBot();
      if (!result.success) {
        alert(`Erro: ${result.message}`);
      }
      onStatusChange();
    } catch (error: any) {
      alert(`Erro ao iniciar bot: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setLoading(true);
    try {
      await apiService.stopBot();
      onStatusChange();
    } catch (error: any) {
      alert(`Erro ao parar bot: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTestMT5 = async () => {
    setMt5Testing(true);
    try {
      const result = await apiService.testMT5Connection();
      if (result.success) {
        alert(`✅ ${result.message}\n\nConta: ${result.account_info?.login || 'N/A'}\nServidor: ${result.account_info?.server || 'N/A'}\nSaldo: $${result.account_info?.balance?.toFixed(2) || '0.00'}`);
      } else {
        alert(`❌ ${result.message}`);
      }
      onStatusChange();
    } catch (error: any) {
      alert(`Erro ao testar conexão: ${error.response?.data?.detail || error.message}`);
    } finally {
      setMt5Testing(false);
    }
  };

  const botRunning = status?.bot_running || false;
  const mt5Connected = status?.mt5_connected || false;

  return (
    <div className="control-panel">
      <h2>🎮 Controle do Bot</h2>

      <div className="status-grid">
        <div className={`status-card ${botRunning ? 'running' : 'stopped'}`}>
          <div className="status-indicator"></div>
          <div className="status-info">
            <h3>Status do Bot</h3>
            <p>{botRunning ? '🟢 Executando' : '🔴 Parado'}</p>
          </div>
        </div>

        <div className={`status-card ${mt5Connected ? 'connected' : 'disconnected'}`}>
          <div className="status-indicator"></div>
          <div className="status-info">
            <h3>Conexão MT5</h3>
            <p>{mt5Connected ? '🟢 Conectado' : '🔴 Desconectado'}</p>
          </div>
        </div>
      </div>

      <div className="control-actions">
        <button
          className="btn btn-primary"
          onClick={handleStart}
          disabled={loading || botRunning || !mt5Connected}
        >
          {loading ? '⏳ Iniciando...' : '▶️ LIGAR BOT'}
        </button>

        <button
          className="btn btn-danger"
          onClick={handleStop}
          disabled={loading || !botRunning}
        >
          {loading ? '⏳ Parando...' : '⏹️ DESLIGAR BOT'}
        </button>

        <button
          className="btn btn-secondary"
          onClick={handleTestMT5}
          disabled={mt5Testing}
        >
          {mt5Testing ? '⏳ Testando...' : '🔌 TESTAR CONEXÃO MT5'}
        </button>
      </div>

      <div className="warning-box">
        <strong>⚠️ ATENÇÃO:</strong> Este sistema opera apenas em conta DEMO. 
        Certifique-se de que o MetaTrader 5 está aberto e logado em uma conta DEMO antes de iniciar o bot.
      </div>
    </div>
  );
};

export default ControlPanel;
