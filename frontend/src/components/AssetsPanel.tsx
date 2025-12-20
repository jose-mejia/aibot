import React, { useState, useEffect } from 'react';
import './AssetsPanel.css';
import { apiService } from '../services/api';

interface Asset {
  symbol: string;
  active: boolean;
  timeframes: string[];
  last_candle_time?: string;
}

const AssetsPanel: React.FC = () => {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [collecting, setCollecting] = useState(false);
  const [collectResult, setCollectResult] = useState<any>(null);

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    try {
      const data = await apiService.getAssets();
      setAssets(data.assets || []);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao carregar ativos:', error);
      setLoading(false);
    }
  };

  const handleToggleActive = (index: number) => {
    const updated = [...assets];
    updated[index].active = !updated[index].active;
    setAssets(updated);
  };

  const handleSymbolChange = (index: number, value: string) => {
    const updated = [...assets];
    updated[index].symbol = value.toUpperCase();
    setAssets(updated);
  };

  const handleTimeframeToggle = (index: number, timeframe: string) => {
    const updated = [...assets];
    const asset = updated[index];
    
    if (asset.timeframes.includes(timeframe)) {
      asset.timeframes = asset.timeframes.filter(tf => tf !== timeframe);
    } else {
      asset.timeframes.push(timeframe);
    }
    
    setAssets(updated);
  };

  const handleAddAsset = () => {
    if (assets.length >= 5) {
      alert('Máximo de 5 ativos permitidos');
      return;
    }
    
    setAssets([
      ...assets,
      { symbol: '', active: true, timeframes: ['H1'] }
    ]);
  };

  const handleRemoveAsset = (index: number) => {
    const updated = assets.filter((_, i) => i !== index);
    setAssets(updated);
  };

  const handleSave = async () => {
    // Validar símbolos únicos
    const symbols = assets.map(a => a.symbol);
    if (new Set(symbols).size !== symbols.length) {
      alert('Símbolos duplicados não são permitidos');
      return;
    }

    // Validar símbolos vazios
    if (assets.some(a => !a.symbol || !a.symbol.trim())) {
      alert('Todos os ativos devem ter um símbolo');
      return;
    }

    setSaving(true);
    try {
      const result = await apiService.updateAssets(assets);
      if (result.success) {
        alert('✅ Ativos salvos com sucesso!');
        loadAssets();
      } else {
        alert(`Erro: ${result.message}`);
      }
    } catch (error: any) {
      alert(`Erro ao salvar: ${error.response?.data?.detail || error.message}`);
    } finally {
      setSaving(false);
    }
  };

  const handleCollectCandles = async () => {
    setCollecting(true);
    setCollectResult(null);
    try {
      const result = await apiService.collectCandles();
      setCollectResult(result);
      if (result.success) {
        loadAssets(); // Recarregar para atualizar last_candle_time
      }
    } catch (error: any) {
      alert(`Erro ao coletar velas: ${error.response?.data?.detail || error.message}`);
    } finally {
      setCollecting(false);
    }
  };

  if (loading) {
    return <div className="assets-panel">Carregando ativos...</div>;
  }

  const activeCount = assets.filter(a => a.active).length;

  return (
    <div className="assets-panel">
      <h2>📊 Ativos Monitorados</h2>
      <p className="panel-description">
        Configure até 5 ativos para monitoramento. A IA coletará velas fechadas automaticamente.
      </p>

      <div className="assets-header">
        <div className="assets-stats">
          <span>Total: {assets.length}/5</span>
          <span>Ativos: {activeCount}</span>
        </div>
        <button
          className="btn-collect"
          onClick={handleCollectCandles}
          disabled={collecting || activeCount === 0}
        >
          {collecting ? '⏳ Coletando...' : '📥 COLETAR VELAS AGORA'}
        </button>
      </div>

      {collectResult && (
        <div className={`collect-result ${collectResult.success ? 'success' : 'error'}`}>
          <strong>Resultado da Coleta:</strong>
          <div>Coletadas: {collectResult.collected}</div>
          <div>Ignoradas: {collectResult.skipped}</div>
          <div>Erros: {collectResult.errors}</div>
        </div>
      )}

      <div className="assets-list">
        {assets.map((asset, index) => (
          <div key={index} className={`asset-card ${asset.active ? 'active' : 'inactive'}`}>
            <div className="asset-header">
              <input
                type="text"
                className="asset-symbol"
                value={asset.symbol}
                onChange={(e) => handleSymbolChange(index, e.target.value)}
                placeholder="Ex: EURUSD"
                maxLength={10}
              />
              <div className="asset-controls">
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    checked={asset.active}
                    onChange={() => handleToggleActive(index)}
                  />
                  <span className="toggle-slider"></span>
                </label>
                <span className={`status-label ${asset.active ? 'active' : 'inactive'}`}>
                  {asset.active ? '✅ Ativo' : '❌ Inativo'}
                </span>
                {assets.length > 1 && (
                  <button
                    className="btn-remove"
                    onClick={() => handleRemoveAsset(index)}
                    title="Remover ativo"
                  >
                    🗑️
                  </button>
                )}
              </div>
            </div>

            <div className="asset-timeframes">
              <label>Timeframes:</label>
              <div className="timeframe-buttons">
                {['H1'].map((tf) => (
                  <button
                    key={tf}
                    className={`timeframe-btn ${asset.timeframes.includes(tf) ? 'selected' : ''}`}
                    onClick={() => handleTimeframeToggle(index, tf)}
                  >
                    {tf}
                  </button>
                ))}
              </div>
            </div>

            {asset.last_candle_time && (
              <div className="asset-last-candle">
                Última vela: {new Date(asset.last_candle_time).toLocaleString('pt-BR')}
              </div>
            )}
          </div>
        ))}

        {assets.length < 5 && (
          <button className="btn-add-asset" onClick={handleAddAsset}>
            + Adicionar Ativo
          </button>
        )}
      </div>

      <button
        className="btn-save-assets"
        onClick={handleSave}
        disabled={saving || assets.length === 0}
      >
        {saving ? '⏳ Salvando...' : '💾 SALVAR CONFIGURAÇÃO'}
      </button>

      <div className="assets-info">
        <h3>ℹ️ Informações</h3>
        <ul>
          <li>Máximo de 5 ativos simultâneos</li>
          <li>Apenas velas fechadas são coletadas</li>
          <li>Timeframe padrão: H1 (1 hora)</li>
          <li>Dados são salvos em: <code>data/market_data/</code></li>
          <li>Coleta automática ocorre quando bot está ligado</li>
        </ul>
      </div>
    </div>
  );
};

export default AssetsPanel;

