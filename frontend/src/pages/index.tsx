// frontend/src/pages/index.tsx
import React, { useEffect, useState } from 'react';
import { getSymbols, getChartData } from '../services/api';
import SelectSymbol from '../components/SelectSymbol';
import Chart from '../components/Chart';

const IndexPage: React.FC = () => {
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selected, setSelected] = useState('BTC/USDT');
  const [chartData, setChartData] = useState<any>(null);

  useEffect(() => {
    getSymbols().then(setSymbols);
  }, []);

  useEffect(() => {
    if (selected) {
      getChartData(selected).then(setChartData);
    }
  }, [selected]);

  return (
    <div>
      <h1>Crypto ML Prediction Dashboard</h1>
      <SelectSymbol symbols={symbols} selected={selected} onChange={setSelected} />
      {chartData && <Chart data={chartData} />}
    </div>
  );
};

export default IndexPage;