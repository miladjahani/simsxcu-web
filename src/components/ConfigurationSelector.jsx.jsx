import React from 'react';
import { CONFIGURATIONS } from '../data/configurations';

const ConfigurationSelector = ({ selectedConfig, onConfigChange, selectedOption, onOptionChange }) => {
  return (
    <div className="card">
      <h2>انتخاب پیکربندی شبیه‌سازی</h2>
      <div className="grid grid-2" style={{ gap: '20px', marginTop: '20px' }}>
        <div>
          <label>پیکربندی:</label>
          <select 
            value={selectedConfig} 
            onChange={(e) => onConfigChange(e.target.value)}
            className="input-blue"
          >
            {Object.entries(CONFIGURATIONS).map(([key, config]) => (
              <option key={key} value={key}>
                {key} - {config.name}
              </option>
            ))}
          </select>
          <div style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
            {CONFIGURATIONS[selectedConfig]?.description}
          </div>
        </div>

        <div>
          <label>گزینه شبیه‌سازی:</label>
          <select 
            value={selectedOption} 
            onChange={(e) => onOptionChange(parseInt(e.target.value))}
            className="input-blue"
          >
            <option value={1}>Option 1 - محاسبه مقدار بهینه v/v%</option>
            <option value={2}>Option 2 - محاسبه پارامترهای کارخانه</option>
          </select>
          <div style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
            {selectedOption === 1 
              ? 'برای استفاده طراحان - محاسبه مقدار بهینه extractant' 
              : 'برای استفاده متالورژیست‌ها - محاسبه پارامترهای کارخانه'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigurationSelector;