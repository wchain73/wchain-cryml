import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend);

interface ChartProps {
  data: any[];
}

const Chart: React.FC<ChartProps> = ({ data }) => {
  const [chartData, setChartData] = useState<any>(null);

  useEffect(() => {
    if (data.length > 0) {
      setChartData({
        labels: data.map(item => item.timestamp),
        datasets: [
          {
            label: 'VWAP',
            data: data.map(item => item.vwap),
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false,
          },
          {
            label: 'Prediction',
            data: data.map(item => item.prediction === '上漲' ? 1 : item.prediction === '下跌' ? -1 : 0),
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false,
          },
        ],
      });
    }
  }, [data]);

  if (!chartData) return <div>Loading...</div>;

  return (
    <div>
      <h2>VWAP and Prediction Trend</h2>
      <Line data={chartData} />
    </div>
  );
};

export default Chart;
