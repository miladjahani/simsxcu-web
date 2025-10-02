import math
import numpy as np
from scipy.optimize import minimize

class SimulationEngine:
    """
    A robust simulation and optimization engine for the SimSXCu process.
    Uses scipy.optimize.minimize to perform optimizations based on engineering goals.
    """

    # --- Core Chemical & Process Calculations ---

    def _calculate_raffinate_cu(self, pls_cu: float, mef1e: float, mef2e: float) -> float:
        """Internal helper to calculate raffinate copper concentration."""
        return pls_cu * (1 - mef1e / 100) * (1 - mef2e / 100)

    def calculate_aml(self, v_v_percent: float) -> float:
        """Calculates AML (Maximum Loading) based on v/v %."""
        if v_v_percent <= 0:
            return 0
        return 0.4108 * math.pow(v_v_percent, 1.1)

    def calculate_ml(self, pls_ac: float, pls_cu: float, v_v_percent: float, aml: float) -> float:
        """Calculates ML (Maximum Loading) based on process parameters."""
        if v_v_percent <= 0 or pls_cu <= 0 or aml <= 0:
            return 0

        term1 = math.pow(pls_ac, 2) / pls_cu
        term2_factor1 = -28.511 * math.pow(v_v_percent, -1.746) * aml + 11.711 * math.pow(v_v_percent, -0.646)
        term2_factor2 = math.pow(3.303 * v_v_percent - 3.0842 * aml, 2) / aml
        term2 = term2_factor1 * term2_factor2

        return term1 - term2

    def calculate_extraction_recovery(self, pls_cu: float, raffinate_cu: float) -> float:
        """Calculates the extraction recovery percentage."""
        if pls_cu == 0:
            return 0
        return ((pls_cu - raffinate_cu) / pls_cu) * 100

    # --- Main Simulation & Optimization Methods ---

    def get_full_simulation_results(self, v_v_percent: float, params: dict) -> dict:
        """
        Calculates all output parameters for a given v/v % and other inputs.
        This is the core calculation function used by both optimization and simulation.
        """
        pls_cu = params['PLS_Cu']
        pls_ac = params['PLS_Ac']

        # Calculate intermediate values
        raffinate_cu = self._calculate_raffinate_cu(pls_cu, params['Mef1e'], params['Mef2e'])
        extraction_recovery = self.calculate_extraction_recovery(pls_cu, raffinate_cu)

        aml = self.calculate_aml(v_v_percent)
        ml = self.calculate_ml(pls_ac, pls_cu, v_v_percent, aml)

        loaded_organic = ml * params['SR'] / 100
        raffinate_ac = pls_ac + (pls_cu - raffinate_cu) * 1.54

        # Placeholder for stripping logic, as per original
        stripped_organic = loaded_organic * 0.4
        stripping_recovery = ((loaded_organic - stripped_organic) / loaded_organic) * 100 if loaded_organic > 0 else 0
        net_transfer = (loaded_organic - stripped_organic) / v_v_percent if v_v_percent > 0 else 0

        return {
            'v/v Percent': v_v_percent,
            'AML': aml,
            'ML': ml,
            'Loaded Organic': loaded_organic,
            'Stripped Organic': stripped_organic,
            'Raffinate Cu': raffinate_cu,
            'Raffinate Ac': raffinate_ac,
            'Extraction Recovery': extraction_recovery,
            'Stripping Recovery': stripping_recovery,
            'Net Transfer': net_transfer,
            'Organic Flow': params['PLS_flow'] * params['Ratio_O_A_Ext']
        }

    def run_optimization(self, params: dict, target_recovery: float = 95.0) -> dict:
        """
        OPTION 1 REFACTORED: Finds the optimal v/v % for a target extraction recovery.
        This version correctly handles the limitations of the provided model.
        """

        # --- Step 1: Check if the target is achievable at all ---
        # Based on the provided model, extraction recovery is independent of v/v %.
        # It only depends on PLS_Cu and mixer efficiencies.

        pls_cu = params['PLS_Cu']
        mef1e = params['Mef1e']
        mef2e = params['Mef2e']

        # Calculate the maximum possible recovery with the given parameters.
        raffinate_cu_at_max_efficiency = self._calculate_raffinate_cu(pls_cu, mef1e, mef2e)
        max_possible_recovery = self.calculate_extraction_recovery(pls_cu, raffinate_cu_at_max_efficiency)

        # --- Step 2: Determine the outcome based on the model's constraints ---

        if max_possible_recovery < target_recovery:
            # The goal is physically impossible with the given mixer efficiencies.
            # Return the results for a nominal v/v % and a clear warning message.
            nominal_vv = params.get('v_v_percent', 10.0)
            results = self.get_full_simulation_results(nominal_vv, params)
            results['Optimization Status'] = 'Failed: Unattainable Target'
            results['Message'] = (
                f"The target recovery of {target_recovery:.1f}% is impossible to achieve. "
                f"With the current mixer efficiencies, the maximum possible recovery is "
                f"{max_possible_recovery:.1f}%. Consider increasing mixer efficiencies."
            )
            results['Target Recovery'] = target_recovery
            return results
        else:
            # The target is achievable. Since recovery is independent of v/v % in this model,
            # and the goal is to minimize extractant concentration, the optimal v/v % is
            # the lowest possible value that is still physically meaningful.
            # We'll use a practical minimum, e.g., 1.0%.
            optimal_vv = 1.0

            results = self.get_full_simulation_results(optimal_vv, params)
            results['Optimization Status'] = 'Success'
            results['Message'] = (
                f"The target recovery of {target_recovery:.1f}% is achievable. "
                f"Within this model, recovery is independent of extractant concentration. "
                f"The minimum practical v/v % ({optimal_vv:.1f}%) has been selected."
            )
            results['Target Recovery'] = target_recovery
            # Overwrite the calculated v/v Percent with the optimal one.
            results['v/v Percent'] = optimal_vv
            return results


    def run_simulation(self, params: dict) -> dict:
        """
        OPTION 2: Runs a direct simulation with all inputs provided by the user.
        """
        v_v_percent = params['v_v_percent']
        results = self.get_full_simulation_results(v_v_percent, params)

        ml = results.get('ML', 0)
        loaded_organic = results.get('Loaded Organic', 0)

        results['Saturation Ratio'] = (loaded_organic / ml) * 100 if ml > 0 else 0
        results['Mixer Efficiency E1'] = params['Mef1e']
        results['Mixer Efficiency E2'] = params['Mef2e']
        return results