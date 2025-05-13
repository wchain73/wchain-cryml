// frontend/src/components/SelectSymbol.tsx
import React from 'react';

type Props = {
  symbols: string[];
  selected: string;
  onChange: (value: string) => void;
};

const SelectSymbol: React.FC<Props> = ({ symbols, selected, onChange }) => {
  return (
    <select value={selected} onChange={(e) => onChange(e.target.value)}>
      {symbols.map((s) => (
        <option key={s} value={s}>
          {s}
        </option>
      ))}
    </select>
  );
};

export default SelectSymbol;