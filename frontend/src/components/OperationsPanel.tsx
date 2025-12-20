import React from 'react';
import './OperationsPanel.css';
import { Trade } from '../services/api';

interface OperationsPanelProps {
  trades: Trade[];
}

const OperationsPanel: React.FC<OperationsPanelProps> = ({ trades }) => {
  const totalProfit = trades
    .filter(t => t.status === 'CLOSED' && t.profit)
    .reduce((sum, t) => sum + (t.profit || 0), 0);

  const openTrades = trades.filter(t => t.status === 'OPEN');
  const closedTrades = trades.filter(t => t.status === 'CLOSED');

  return (
    <div className="operations-panel">
      <h2>📈 Operações</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Lucro/Prejuízo Total</h3>
          <p className={totalProfit >= 0 ? 'profit' : 'loss'}>
            ${totalProfit.toFixed(2)}
          </p>
        </div>
        <div className="stat-card">
          <h3>Operações Abertas</h3>
          <p>{openTrades.length}</p>
        </div>
        <div className="stat-card">
          <h3>Operações Fechadas</h3>
          <p>{closedTrades.length}</p>
        </div>
        <div className="stat-card">
          <h3>Total de Operações</h3>
          <p>{trades.length}</p>
        </div>
      </div>

      <div className="trades-section">
        <h3>Tabela de Operações</h3>
        {trades.length === 0 ? (
          <p className="empty-state">Nenhuma operação ainda</p>
        ) : (
          <div className="trades-table">
            <table>
              <thead>
                <tr>
                  <th>Data/Hora</th>
                  <th>Par</th>
                  <th>Tipo</th>
                  <th>Preço Entrada</th>
                  <th>Preço Saída</th>
                  <th>SL</th>
                  <th>TP</th>
                  <th>Resultado</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {trades.slice().reverse().map((trade) => (
                  <tr key={trade.id}>
                    <td>{new Date(trade.open_time).toLocaleString('pt-BR')}</td>
                    <td>{trade.symbol}</td>
                    <td>
                      <span className={`trade-type ${trade.type.toLowerCase()}`}>
                        {trade.type}
                      </span>
                    </td>
                    <td>${trade.entry_price.toFixed(5)}</td>
                    <td>{trade.exit_price ? `$${trade.exit_price.toFixed(5)}` : '-'}</td>
                    <td>{trade.stop_loss}</td>
                    <td>{trade.take_profit}</td>
                    <td>
                      {trade.profit !== undefined && (
                        <span className={trade.profit >= 0 ? 'profit' : 'loss'}>
                          ${trade.profit.toFixed(2)}
                        </span>
                      )}
                      {trade.profit === undefined && '-'}
                    </td>
                    <td>
                      <span className={`status-badge ${trade.status.toLowerCase()}`}>
                        {trade.status === 'OPEN' ? 'Aberta' : trade.status === 'CLOSED' ? 'Fechada' : 'Cancelada'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default OperationsPanel;

