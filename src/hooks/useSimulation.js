import { useState, useCallback } from 'react';
import { SimulationEngine } from '../utils/calculations';

export const useSimulation = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [chartData, setChartData] = useState([]);

  const runSimulation = useCallback(async (configuration, option, parameters) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // شبیه‌سازی غیرهمزمان
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const engine = new SimulationEngine(configuration, option);
      let simulationResults;
      
      if (option === 1) {
        simulationResults = engine.simulateOption1(parameters);
      } else {
        simulationResults = engine.simulateOption2(parameters);
      }
      
      const chartData = engine.generateChartData(simulationResults, parameters);
      
      setResults(simulationResults);
      setChartData(chartData);
      
    } catch (err) {
      setError('خطا در انجام شبیه‌سازی: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const resetSimulation = useCallback(() => {
    setResults(null);
    setChartData([]);
    setError(null);
  }, []);

  return {
    isLoading,
    results,
    error,
    chartData,
    runSimulation,
    resetSimulation
  };
};