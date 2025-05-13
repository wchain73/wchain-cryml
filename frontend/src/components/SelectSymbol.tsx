import React from 'react';

interface SelectSymbolProps {
  symbols: string[];
  onSelect: (symbol: string) => void;
}

const SelectSymbol: React.FC<SelectSymbolProps> = ({ symbols, onSelect }) => {
  return (
    <div>
      <select onChange={(e) => onSelect(e.target.value)}>
        {symbols.map((symbol) => (
          <option key={symbol} value={symbol}>
            {symbol}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SelectSymbol;
