import { describe, it, expect } from 'vitest';
import { SimulationEngine } from '../utils/calculations';

describe('SimulationEngine', () => {
  it('should handle v_v_percent being zero in calculateML', () => {
    const engine = new SimulationEngine('A', 1);
    const result = engine.calculateML(10, 5, 0, 20);
    expect(result).not.toBe(Infinity);
    expect(result).not.toBeNaN();
  });
});