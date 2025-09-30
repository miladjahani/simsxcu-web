import React, { useState } from 'react';
import { useSimulation } from './hooks/useSimulation';
import ConfigurationSelector from './components/ConfigurationSelector';
import ParameterInput from './components/ParameterInput';
import ResultsDisplay from './components/ResultsDisplay';
import Charts from './components/Charts';
import { DEFAULT_PARAMETERS } from './data/configurations';

function App() {
  const [selectedConfig, setSelectedConfig] = useState('A');
  const [selectedOption, setSelectedOption] = useState(1);
  const [parameters, setParameters] = useState(DEFAULT_PARAMETERS);
  
  const { isLoading, results, error, chartData, runSimulation, resetSimulation } = useSimulation();

  const handleRunSimulation = () => {
    runSimulation(selectedConfig, selectedOption, parameters);
  };

  const handleReset = () => {
    resetSimulation();
    setParameters(DEFAULT_PARAMETERS);
  };

  return (
    <div className="container">
      <header style={{ textAlign: 'center', marginBottom: '30px', color: 'white' }}>
        <h1>SimSXCu - نسخه تحت وب</h1>
        <p>شبیه‌ساز استخراج حلال مس با Lix984N</p>
        <div style={{ fontSize: '14px', opacity: 0.9 }}>
          © 2016 Joseph Kafumbila - توسعه یافته برای دسترسی آنلاین
        </div>
      </header>

      <ConfigurationSelector
        selectedConfig={selectedConfig}
        onConfigChange={setSelectedConfig}
        selectedOption={selectedOption}
        onOptionChange={setSelectedOption}
      />

      <ParameterInput
        parameters={parameters}
        onParameterChange={setParameters}
        selectedOption={selectedOption}
      />

      <div className="card">
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          <button 
            onClick={handleRunSimulation} 
            className="btn"
            disabled={isLoading}
          >
            {isLoading ? 'در حال شبیه‌سازی...' : 'اجرای شبیه‌سازی'}
          </button>
          
          <button 
            onClick={handleReset}
            className="btn"
            style={{ background: 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)' }}
          >
            بازنشانی
          </button>
        </div>
      </div>

      <ResultsDisplay 
        results={results}
        isLoading={isLoading}
        error={error}
      />

      <Charts 
        chartData={chartData}
        selectedOption={selectedOption}
      />

      <footer style={{ textAlign: 'center', marginTop: '40px', color: 'white', opacity: 0.8 }}>
        <p>SimSXCu Full Version 2.0 - توسعه یافته برای GitHub Pages</p>
        <p>jokafumbila@hotmail.com</p>
      </footer>
    </div>
  );
}

export default App;