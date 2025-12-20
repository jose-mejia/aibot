import React, { useState, useEffect } from 'react';
import './ConfigPanel.css';
import { apiService, BotConfig } from '../services/api';

interface ConfigPanelProps {
  onConfigChange: () => void;
}

const ConfigPanel: React.FC<ConfigPanelProps> = ({ onConfigChange }) => {
  const [config, setConfig] = useState<Partial<BotConfig>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const data = await apiService.getConfig();
      setConfig(data);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar configurações:', error);
      setLoading(false);
    }
  };

  const handleChange = (field: keyof BotConfig, value: any) => {
    setConfig({ ...config, [field]: value });
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const result = await apiService.updateConfig(config);
      if (result.success) {
        alert('✅ Configurações salvas com sucesso!');
        onConfigChange();
      } else {
        alert(`Erro: ${result.message}`);
      }
    } catch (error: any) {
      alert(`Erro ao salvar: ${error.response?.data?.detail || error.message}`);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="config-panel">Carregando configurações...</div>;
  }

  return (
    <div className="config-panel">
      <h2>⚙️ Configurações do MT5</h2>
      <p className="config-warning">⚠️ Pare o bot antes de alterar as configurações</p>

      <div className="config-form">
        <div className="form-group">
          <label>Par de Negociação</label>
          <input
            type="text"
            value={config.symbol || 'EURUSD'}
            onChange={(e) => handleChange('symbol', e.target.value.toUpperCase())}
            disabled
            title="Fixado em EURUSD inicialmente"
          />
        </div>

        <div className="form-group">
          <label>Timeframe</label>
          <select
            value={config.timeframe || 'M15'}
            onChange={(e) => handleChange('timeframe', e.target.value)}
          >
            <option value="M1">M1 (1 minuto)</option>
            <option value="M5">M5 (5 minutos)</option>
            <option value="M15">M15 (15 minutos)</option>
            <option value="M30">M30 (30 minutos)</option>
            <option value="H1">H1 (1 hora)</option>
          </select>
        </div>

        <div className="form-group">
          <label>Volume (Lote)</label>
          <input
            type="number"
            step="0.01"
            min="0.01"
            max="100"
            value={config.volume || 0.01}
            onChange={(e) => handleChange('volume', parseFloat(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label>Stop Loss (pontos)</label>
          <input
            type="number"
            min="10"
            value={config.stop_loss || 50}
            onChange={(e) => handleChange('stop_loss', parseInt(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label>Take Profit (pontos)</label>
          <input
            type="number"
            min="10"
            value={config.take_profit || 100}
            onChange={(e) => handleChange('take_profit', parseInt(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label>Magic Number</label>
          <input
            type="number"
            value={config.magic_number || 234000}
            onChange={(e) => handleChange('magic_number', parseInt(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label>Máximo de Trades Simultâneos</label>
          <input
            type="number"
            min="1"
            max="10"
            value={config.max_simultaneous_trades || 1}
            onChange={(e) => handleChange('max_simultaneous_trades', parseInt(e.target.value))}
          />
        </div>

        <div className="form-group">
          <label>Intervalo de Análise (segundos)</label>
          <input
            type="number"
            min="10"
            value={config.analysis_interval || 60}
            onChange={(e) => handleChange('analysis_interval', parseInt(e.target.value))}
          />
        </div>
      </div>

      <button
        className="btn-save"
        onClick={handleSave}
        disabled={saving}
      >
        {saving ? '⏳ Salvando...' : '💾 SALVAR CONFIGURAÇÕES'}
      </button>
    </div>
  );
};

export default ConfigPanel;
