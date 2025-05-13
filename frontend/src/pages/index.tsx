import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import SelectSymbol from '../components/SelectSymbol';
import Chart from '../components/Chart';

const IndexPage: React.FC = () => {
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string>('');
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    // 這裡請換成從後端 API 獲取支持的交易對
    setSymbols(['BTC/USDT', 'ETH/USDT']);
    setSelectedSymbol('BTC/USDT');
  }, []);

  useEffect(() => {
    if (selectedSymbol) {
      api.getChartData(selectedSymbol).then((data) => setChartData(data));
    }
  }, [selectedSymbol]);

  return (
    <div>
      <h1>Crypto Prediction Dashboard</h1>
      <SelectSymbol symbols={symbols} onSelect={setSelectedSymbol} />
      <Chart data={chartData} />
    </div>
  );
};

export default IndexPage;
