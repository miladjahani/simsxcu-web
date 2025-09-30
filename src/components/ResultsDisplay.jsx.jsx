import React from 'react';

const ResultsDisplay = ({ results, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="card">
        <div className="loading">
          <div>در حال انجام شبیه‌سازی...</div>
          <div style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
            این process ممکن است چند ثانیه طول بکشد
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">{error}</div>
      </div>
    );
  }

  if (!results) {
    return null;
  }

  return (
    <div className="card">
      <h2>نتایج شبیه‌سازی</h2>
      
      <div className="success" style={{ marginBottom: '20px' }}>
        شبیه‌سازی با موفقیت انجام شد!
      </div>

      <div className="grid grid-3">
        <div className="input-group">
          <label>مقدار بهینه v/v%</label>
          <div style={{ 
            padding: '10px', 
            background: '#f8f9fa', 
            borderRadius: '6px',
            fontWeight: 'bold',
            color: '#2c3e50'
          }}>
            {results.optimum_v_v_percent?.toFixed(2)}%
          </div>
        </div>

        <div className="input-group">
          <label>AML</label>
          <div style={{ padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
            {results.AML?.toFixed(2)} g/l Cu
          </div>
        </div>

        <div className="input-group">
          <label>ML</label>
          <div style={{ padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
            {results.ML?.toFixed(2)} g/l Cu
          </div>
        </div>

        <div className="input-group">
          <label>بار آلی</label>
          <div style={{ padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
            {results.loaded_organic?.toFixed(2)} g/l Cu
          </div>
        </div>

        <div className="input-group">
          <label>بازیابی استخراج</label>
          <div style={{ padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
            {results.extraction_recovery?.toFixed(1)}%
          </div>
        </div>

        <div className="input-group">
          <label>بازیابی stripping</label>
          <div style={{ padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
            {results.stripping_recovery?.toFixed(1)}%
          </div>
        </div>

        {results.saturation_ratio && (
          <div className="input-group">
            <label>نسبت اشباع</label>
            <div style={{ padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
              {results.saturation_ratio?.toFixed(1)}%
            </div>
          </div>
        )}

        <div className="input-group">
          <label>انتقال خالص</label>
          <div style={{ padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
            {results.net_transfer?.toFixed(3)} g/l per 1% extractant
          </div>
        </div>

        <div className="input-group">
          <label>جریان آلی</label>
          <div style={{ padding: '10px', background: '#f8f9fa', borderRadius: '6px' }}>
            {results.organic_flow?.toFixed(0)} m³/h
          </div>
        </div>
      </div>

      {results.raffinate_Cu && (
        <div style={{ marginTop: '20px', padding: '16px', background: '#f8f9fa', borderRadius: '8px' }}>
          <h3>Raffinate</h3>
          <div className="grid grid-2">
            <div className="input-group">
              <label>مس</label>
              <div style={{ padding: '8px', background: 'white', borderRadius: '4px' }}>
                {results.raffinate_Cu?.toFixed(2)} g/l
              </div>
            </div>
            <div className="input-group">
              <label>اسید</label>
              <div style={{ padding: '8px', background: 'white', borderRadius: '4px' }}>
                {results.raffinate_Ac?.toFixed(2)} g/l
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;