// frontend/src/services/api.ts
import axios from 'axios';

export const getSymbols = async (): Promise<string[]> => {
  const res = await axios.get('/api/symbols');
  return res.data;
};

export const getChartData = async (symbol: string): Promise<any> => {
  const res = await axios.get('/api/chart', { params: { symbol } });
  return res.data;
};