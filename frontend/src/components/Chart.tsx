// frontend/src/components/Chart.tsx
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

type Props = {
  data: {
    labels: string[];
    vwap_diff: number[];
    prediction: string[];
  };
};

const Chart: React.FC<Props> = ({ data }) => {
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: 'VWAP Diff',
        data: data.vwap_diff,
        borderColor: 'rgba(75,192,192,1)',
        fill: false
      },
      {
        label: 'Prediction',
        data: data.prediction.map((val) => (val === '上漲' ? 1 : val === '下跌' ? -1 : 0)),
        borderColor: 'rgba(255,99,132,1)',
        fill: false
      }
    ]
  };

  return <Line data={chartData} />;
};

export default Chart;
