import React from 'react';
import { DEFAULT_PARAMETERS } from '../data/configurations';

const ParameterInput = ({ parameters, onParameterChange, selectedOption }) => {
  const handleChange = (key, value) => {
    onParameterChange({
      ...parameters,
      [key]: parseFloat(value) || 0
    });
  };

  const getInputClass = (key) => {
    // تعیین رنگ بر اساس نوع پارامتر (مشابه اکسل)
    if (['PLS_flow', 'PLS_Cu', 'PLS_Ac', 'SR', 'SP_Cu', 'SPAc', 'AD_Cu'].includes(key)) {
      return 'input-red';
    } else if (key === 'v_v_percent' && selectedOption === 1) {
      return 'input-blue';
    }
    return '';
  };

  const parameterLabels = {
    PLS_flow: 'جریان PLS (m³/h)',
    PLS_Cu: 'غلظت مس PLS (g/l)',
    PLS_Ac: 'غلظت اسید PLS (g/l)',
    SR: 'نسبت اشباع (%)',
    Ratio_O_A_Ext: 'نسبت O/A استخراج',
    Mef1e: 'راندمان میکسر استخراج ۱ (%)',
    Mef2e: 'راندمان میکسر استخراج ۲ (%)',
    SP_Cu: 'مس الکترولیت مصرف شده (g/l)',
    SPAc: 'اسید الکترولیت مصرف شده (g/l)',
    AD_Cu: 'مس الکترولیت پیشرفته (g/l)',
    Mef1s: 'راندمان میکسر stripping ۱ (%)',
    v_v_percent: 'درصد حجمی extractant (%)'
  };

  return (
    <div className="card">
      <h2>پارامترهای ورودی</h2>
      <div style={{ marginBottom: '16px', fontSize: '14px', color: '#666' }}>
        <span style={{ color: '#e74c3c' }}>■ قرمز: </span>ورودی کاربر | 
        <span style={{ color: '#3498db' }}> ■ آبی: </span>متغیر محاسباتی | 
        <span style={{ color: '#27ae60' }}> ■ سبز: </span>محدودیت‌ها
      </div>
      
      <div className="grid grid-3">
        {Object.entries(DEFAULT_PARAMETERS).map(([key, defaultValue]) => (
          <div key={key} className="input-group">
            <label>{parameterLabels[key]}</label>
            <input
              type="number"
              step="0.01"
              value={parameters[key] || ''}
              onChange={(e) => handleChange(key, e.target.value)}
              className={getInputClass(key)}
              placeholder={defaultValue.toString()}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ParameterInput;