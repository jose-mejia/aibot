import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface BotConfig {
  symbol: string;
  timeframe: string;
  volume: number;
  stop_loss: number;
  take_profit: number;
  magic_number: number;
  max_simultaneous_trades: number;
  analysis_interval: number;
  demo_mode: boolean;
}

export interface Trade {
  id: string;
  symbol: string;
  type: 'BUY' | 'SELL';
  entry_price: number;
  exit_price?: number;
  volume: number;
  stop_loss: number;
  take_profit: number;
  profit?: number;
  status: 'OPEN' | 'CLOSED' | 'CANCELLED';
  open_time: string;
  close_time?: string;
}

export interface LogEntry {
  level: 'INFO' | 'WARNING' | 'ERROR' | 'DEBUG';
  message: string;
  timestamp: string;
  source?: string;
}

export const apiService = {
  getStatus: async () => {
    const response = await api.get('/api/status');
    return response.data;
  },

  startBot: async () => {
    const response = await api.post('/api/bot/start');
    return response.data;
  },

  stopBot: async () => {
    const response = await api.post('/api/bot/stop');
    return response.data;
  },

  getConfig: async () => {
    const response = await api.get('/api/config');
    return response.data;
  },

  updateConfig: async (config: Partial<BotConfig>) => {
    const response = await api.post('/api/config', config);
    return response.data;
  },

  getTrades: async (limit: number = 50) => {
    const response = await api.get(`/api/trades?limit=${limit}`);
    return response.data.trades || [];
  },

  getLogs: async (limit: number = 100) => {
    const response = await api.get(`/api/logs?limit=${limit}`);
    return response.data.logs || [];
  },

  testMT5Connection: async () => {
    const response = await api.post('/api/mt5/test');
    return response.data;
  },
};
