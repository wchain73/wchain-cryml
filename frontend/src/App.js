import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// 註冊 Chart.js 所需的元件
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  // 設定初始狀態
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Price',
        data: [],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
      {
        label: 'VWAP',
        data: [],
        borderColor: 'rgba(153, 102, 255, 1)',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
      },
      {
        label: 'Prediction',
        data: [],
        borderColor: 'rgba(255, 159, 64, 1)',
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
      },
    ],
  });

  const [symbol, setSymbol] = useState('BTC/USDT'); // 預設交易對為 BTC/USDT

  // 當 symbol 改變時重新獲取資料
  useEffect(() => {
    fetch(`/api/chart?symbol=${symbol}`)
      .then(response => response.json())
      .then(data => {
        setChartData({
          labels: data.timestamp,
          datasets: [
            {
              label: 'Price',
              data: data.price,
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
            },
            {
              label: 'VWAP',
              data: data.vwap,
              borderColor: 'rgba(153, 102, 255, 1)',
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
            },
            {
              label: 'Prediction',
              data: data.prediction,
              borderColor: 'rgba(255, 159, 64, 1)',
              backgroundColor: 'rgba(255, 159, 64, 0.2)',
            },
          ],
        });
      })
      .catch(error => console.error('Error fetching chart data:', error));
  }, [symbol]); // 當 symbol 改變時觸發

  return (
    <div style={{ padding: '20px' }}>
      <h1>Crypto Machine Learning Prediction</h1>
      <div>
        <label htmlFor="symbol">Select Trading Pair: </label>
        <select
          id="symbol"
          onChange={e => setSymbol(e.target.value)}
          value={symbol}
        >
          <option value="BTC/USDT">BTC/USDT</option>
          <option value="ETH/USDT">ETH/USDT</option>
          <option value="SOL/USDT">SOL/USDT</option>
          {/* 可以繼續擴充其他交易對 */}
        </select>
      </div>
      <div style={{ marginTop: '20px' }}>
        <Line data={chartData} options={{ responsive: true }} />
      </div>
    </div>
  );
}

export default App;
