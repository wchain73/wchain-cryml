import axios from 'axios';

const API_URL = 'https://your-backend-url.com'; // 請換成你的後端 URL

export const api = {
  getChartData: async (symbol: string) => {
    try {
      const response = await axios.get(`${API_URL}/chart/${symbol}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching chart data:', error);
      return [];
    }
  },
};
