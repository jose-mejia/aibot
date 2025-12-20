import React from 'react';
import './LogsPanel.css';
import { LogEntry } from '../services/api';

interface LogsPanelProps {
  logs: LogEntry[];
}

const LogsPanel: React.FC<LogsPanelProps> = ({ logs }) => {
  return (
    <div className="logs-panel">
      <h2>📝 Logs do Sistema</h2>
      <p className="logs-description">
        Logs em tempo real do sistema, incluindo decisões da IA, erros e execução de ordens.
      </p>

      <div className="logs-container">
        {logs.length === 0 ? (
          <p className="empty-state">Nenhum log ainda</p>
        ) : (
          logs.slice().reverse().map((log, index) => (
            <div key={index} className={`log-entry log-${log.level.toLowerCase()}`}>
              <span className="log-time">
                {new Date(log.timestamp).toLocaleTimeString('pt-BR')}
              </span>
              <span className="log-level">{log.level}</span>
              <span className="log-source">{log.source || 'System'}</span>
              <span className="log-message">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LogsPanel;

