import numpy as np
import pandas as pd
from scipy.optimize import minimize, fsolve
from typing import Dict, List, Tuple, Optional

class SimSXCu:
    """
    Copper Solvent Extraction Simulation Engine
    Full Version 2.0 - Based on Joseph Kafumbila's SimSXCu
    """

    def __init__(self):
        self.configurations = {
            'A': 'Series 2Ex1S',
            'B': 'Series 2Ex2S',
            'C': 'Series 3Ex1S',
            'D': 'Series 3Ex2S',
            'E': 'Series parallel 2Ex1Px1S',
            'F': 'Series parallel 2Ex1Px2S',
            'G': 'Optimum series parallel 1Ex1Px1Ex1S',
            'H': 'Optimum series parallel 1Ex1Px1Ex2S',
            'I': 'Triple parallel 1Ex1Px1Px1S',
            'J': 'Triple parallel 1Ex1Px1Px2S',
            'K': 'Interlaced 1Ex1Px1Ex1Px1S',
            'L': 'Interlaced 1Ex1Px1Ex1Px2S',
            'M': 'Double series parallel 2Ex2Px1S',
            'N': 'Double series parallel 2Ex2Px2S',
            'O': 'Optimum triple parallel 1Ex1Px1Px1Ex1S',
            'P': 'Optimum triple parallel 1Ex1Px1Px1Ex2S',
            'Q': 'Organic by pass 2Ex2Px1S',
            'R': 'Organic by pass 2Ex2Px2S'
        }

        self.extractant = "Lix984N"

    def calculate_AML(self, v_v_percent: float) -> float:
        """
        Calculate AML (Maximum loaded when free acid concentration in PLS is zero)
        AML = 0.4108 * (v/v%)^1.1
        """
        return 0.4108 * (v_v_percent ** 1.1)

    def extraction_equilibrium(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float, C_org: float) -> float:
        """
        Calculate extraction equilibrium using the complex formula from Excel
        This represents the relationship between aqueous and organic copper concentrations
        """
        term1 = -28.511 * (v_v_percent ** -1.746) * C_org + 11.711 * (v_v_percent ** -0.646)
        term2 = (3.303 * v_v_percent - 3.0842 * C_org) ** 2 / C_org
        inner_term = term1 * term2

        A = -1.299 * PLS_Ac - 2 * PLS_Cu - 0.422 * inner_term
        B = ((A ** 2) - 4 * ((0.644 * PLS_Ac + PLS_Cu) ** 2)) ** 0.5

        C_aq = (-A - B) / 2
        return C_aq

    def stripping_equilibrium(self, SP_Cu: float, SP_Ac: float, v_v_percent: float, C_org: float) -> float:
        """
        Calculate stripping equilibrium using the formula from Excel
        """
        term1 = (4.8579/1000 * v_v_percent - 0.19183) * C_org + 11.365 * (v_v_percent ** -0.85)
        term2 = (3.303 * v_v_percent - 3.0842 * C_org) ** 2 / C_org
        inner_term = term1 * term2

        A = -1.299 * SP_Ac - 2 * SP_Cu - 0.422 * inner_term
        B = ((A ** 2) - 4 * ((0.644 * SP_Ac + SP_Cu) ** 2)) ** 0.5

        C_aq = (-A - B) / 2
        return C_aq

    def calculate_ML(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float, C_org: float) -> float:
        """
        Calculate ML (Maximum loaded - value of copper concentration in organic phase in steady state with PLS)
        """
        equilibrium_term = self.extraction_equilibrium(PLS_Cu, PLS_Ac, v_v_percent, C_org)
        return (PLS_Ac ** 2 / PLS_Cu) - equilibrium_term

    def extraction_recovery(self, PLS_Cu: float, raffinate_Cu: float) -> float:
        """
        Calculate extraction recovery percentage
        """
        return ((PLS_Cu - raffinate_Cu) / PLS_Cu) * 100

    def stripping_recovery(self, loaded_organic_Cu: float, stripped_organic_Cu: float) -> float:
        """
        Calculate stripping recovery percentage
        """
        return ((loaded_organic_Cu - stripped_organic_Cu) / loaded_organic_Cu) * 100

    def net_transfer(self, loaded_organic_Cu: float, stripped_organic_Cu: float, v_v_percent: float) -> float:
        """
        Calculate net transfer (g/l per 1% extractant)
        """
        return (loaded_organic_Cu - stripped_organic_Cu) / v_v_percent

class ConfigurationA_2Ex1S:
    """
    Configuration A: Series 2Ex1S (2 Extraction stages, 1 Stripping stage)
    """

    def __init__(self, sim_engine: SimSXCu):
        self.sim = sim_engine
        self.name = "Series 2Ex1S"

    def option1_objective(self, x: List[float], params: Dict) -> float:
        """
        Objective function for Option 1 - Find optimum extractant volume percentage
        x[0] = v/v%
        """
        v_v_percent = x[0]

        # Extract parameters
        PLS_flow = params['PLS_flow']
        PLS_Cu = params['PLS_Cu']
        PLS_Ac = params['PLS_Ac']
        SR = params['SR']
        O_A_Ext = params['O_A_Ext']
        Mef1e = params['Mef1e']
        Mef2e = params['Mef2e']
        SP_Cu = params['SP_Cu']
        SP_Ac = params['SP_Ac']
        AD_Cu = params['AD_Cu']
        Mef1s = params['Mef1s']

        # Calculate intermediate values
        AML = self.sim.calculate_AML(v_v_percent)
        ML = AML * SR / 100
        LO = ML  # Loaded organic

        # Calculate extraction stage concentrations (simplified)
        # These would need the full complex calculations from the Excel
        C1Cuor_Ext = self.calculate_C1Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, O_A_Ext, LO)
        C2Cuor_Ext = self.calculate_C2Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, Mef2e, O_A_Ext, LO, C1Cuor_Ext)

        # Calculate stripping stage
        O_A_str = self.calculate_O_A_str(AD_Cu, SP_Cu, LO, C2Cuor_Ext, O_A_Ext, PLS_Cu, PLS_Ac, v_v_percent, Mef1e, Mef2e, C1Cuor_Ext)
        C1Cuor_Str = self.calculate_C1Cuor_Str(SP_Cu, SP_Ac, v_v_percent, LO, Mef1s, O_A_str, AD_Cu)

        # Objective: Balance between stripping output and extraction input
        objective = (C1Cuor_Str * Mef1s / 100 + LO * (1 - Mef1s / 100)) - C2Cuor_Ext

        return abs(objective)

    def option2_objective(self, x: List[float], params: Dict) -> float:
        """
        Objective function for Option 2 - Find plant parameters
        x[0] = v/v%, x[1] = saturation ratio, x[2] = mixer efficiency 1, x[3] = mixer efficiency 2
        """
        v_v_percent = x[0]
        SR = x[1]
        Mef1e = x[2]
        Mef2e = x[3]

        # Extract fixed parameters
        PLS_flow = params['PLS_flow']
        PLS_Cu = params['PLS_Cu']
        PLS_Ac = params['PLS_Ac']
        O_A_Ext = params['O_A_Ext']
        ML_plant = params['ML_plant']
        SP_Cu = params['SP_Cu']
        SP_Ac = params['SP_Ac']
        AD_Cu = params['AD_Cu']
        Mef1s = params['Mef1s']

        # Calculate values
        AML = self.sim.calculate_AML(v_v_percent)
        LO = ML_plant * SR / 100

        # Calculate extraction stages
        C1Cuor_Ext = self.calculate_C1Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, O_A_Ext, LO)
        C2Cuor_Ext = self.calculate_C2Cuor_Ext(PLS_Cu, PLS_Ac, v_v_percent, Mef1e, Mef2e, O_A_Ext, LO, C1Cuor_Ext)

        # Calculate raffinate
        raffinate_E1 = self.calculate_raffinate_E1(PLS_Cu, PLS_Ac, v_v_percent, C1Cuor_Ext, Mef1e)
        raffinate_E2 = self.calculate_raffinate_E2(PLS_Cu, PLS_Ac, v_v_percent, C2Cuor_Ext, Mef2e, raffinate_E1)

        # Calculate stripping
        O_A_str = self.calculate_O_A_str(AD_Cu, SP_Cu, LO, C2Cuor_Ext, O_A_Ext, PLS_Cu, PLS_Ac, v_v_percent, Mef1e, Mef2e, C1Cuor_Ext)
        C1Cuor_Str = self.calculate_C1Cuor_Str(SP_Cu, SP_Ac, v_v_percent, LO, Mef1s, O_A_str, AD_Cu)

        # Multiple objectives
        obj1 = ML_plant - self.sim.calculate_ML(PLS_Cu, PLS_Ac, v_v_percent, C1Cuor_Ext)
        obj2 = raffinate_E2 - params['raffinate_Cu_target']
        obj3 = C1Cuor_Str - params['stripped_organic_Cu_target']

        return abs(obj1) + abs(obj2) + abs(obj3)

    def calculate_C1Cuor_Ext(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float,
                           Mef1e: float, O_A_Ext: float, LO: float) -> float:
        """
        Calculate copper in organic after first extraction stage
        """
        # Simplified calculation - would need full formula from Excel
        C_eq = self.sim.extraction_equilibrium(PLS_Cu, PLS_Ac, v_v_percent, LO)
        transfer = C_eq * Mef1e / 100
        C_org = LO + transfer / O_A_Ext
        return C_org

    def calculate_C2Cuor_Ext(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float,
                           Mef1e: float, Mef2e: float, O_A_Ext: float, LO: float,
                           C1Cuor_Ext: float) -> float:
        """
        Calculate copper in organic after second extraction stage
        """
        # Simplified calculation
        raffinate_E1 = PLS_Cu - (C1Cuor_Ext - LO) * O_A_Ext
        C_eq = self.sim.extraction_equilibrium(raffinate_E1, PLS_Ac, v_v_percent, LO)
        transfer = C_eq * Mef2e / 100
        C_org = C1Cuor_Ext + transfer / O_A_Ext
        return C_org

    def calculate_O_A_str(self, AD_Cu: float, SP_Cu: float, LO: float, C2Cuor_Ext: float,
                        O_A_Ext: float, PLS_Cu: float, PLS_Ac: float, v_v_percent: float,
                        Mef1e: float, Mef2e: float, C1Cuor_Ext: float) -> float:
        """
        Calculate O/A ratio for stripping
        """
        # Mass balance approach
        copper_to_strip = LO - C2Cuor_Ext
        copper_transfer = AD_Cu - SP_Cu
        O_A_str = copper_transfer / copper_to_strip if copper_to_strip != 0 else 1.0
        return O_A_str

    def calculate_C1Cuor_Str(self, SP_Cu: float, SP_Ac: float, v_v_percent: float,
                           LO: float, Mef1s: float, O_A_str: float, AD_Cu: float) -> float:
        """
        Calculate copper in organic after stripping
        """
        # Simplified calculation
        C_eq = self.sim.stripping_equilibrium(SP_Cu, SP_Ac, v_v_percent, LO)
        transfer = C_eq * Mef1s / 100
        C_org = LO - transfer * O_A_str
        return C_org

    def calculate_raffinate_E1(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float,
                             C_org: float, Mef1e: float) -> float:
        """
        Calculate raffinate after first extraction
        """
        C_eq = self.sim.extraction_equilibrium(PLS_Cu, PLS_Ac, v_v_percent, C_org)
        raffinate = C_eq * Mef1e / 100 + PLS_Cu * (1 - Mef1e / 100)
        return raffinate

    def calculate_raffinate_E2(self, PLS_Cu: float, PLS_Ac: float, v_v_percent: float,
                             C_org: float, Mef2e: float, raffinate_E1: float) -> float:
        """
        Calculate raffinate after second extraction
        """
        C_eq = self.sim.extraction_equilibrium(raffinate_E1, PLS_Ac, v_v_percent, C_org)
        raffinate = C_eq * Mef2e / 100 + raffinate_E1 * (1 - Mef2e / 100)
        return raffinate

class SolverEngine:
    """
    Solver engine to optimize parameters
    """

    def __init__(self):
        self.method = 'SLSQP'  # Sequential Least Squares Programming

    def solve_option1(self, objective_func, initial_guess: List[float],
                     bounds: List[Tuple], params: Dict) -> Dict:
        """
        Solve Option 1: Find optimum extractant volume percentage
        """
        result = minimize(
            objective_func,
            initial_guess,
            args=(params,),
            method=self.method,
            bounds=bounds,
            options={'ftol': 1e-8, 'disp': True}
        )

        return {
            'success': result.success,
            'v_v_percent': result.x[0],
            'objective_value': result.fun,
            'message': result.message
        }

    def solve_option2(self, objective_func, initial_guess: List[float],
                     bounds: List[Tuple], params: Dict) -> Dict:
        """
        Solve Option 2: Find plant parameters
        """
        result = minimize(
            objective_func,
            initial_guess,
            args=(params,),
            method=self.method,
            bounds=bounds,
            options={'ftol': 1e-8, 'disp': True}
        )

        return {
            'success': result.success,
            'v_v_percent': result.x[0],
            'saturation_ratio': result.x[1],
            'mixer_eff1': result.x[2],
            'mixer_eff2': result.x[3],
            'objective_value': result.fun,
            'message': result.message
        }

# Example usage and test cases
def main():
    # Initialize the simulation engine
    sim_engine = SimSXCu()
    config_A = ConfigurationA_2Ex1S(sim_engine)
    solver = SolverEngine()

    print("SimSXCu Copper Solvent Extraction Simulation")
    print("Full Version 2.0 - Python Implementation")
    print("=" * 50)

    # Test Option 1 - Designer mode
    print("\nOption 1 - Designer Mode (Optimum Extractant Percentage)")

    params_option1 = {
        'PLS_flow': 400,      # m³/h
        'PLS_Cu': 2.5,        # g/l
        'PLS_Ac': 1.6,        # g/l
        'SR': 92,             # %
        'O_A_Ext': 1,         # -
        'Mef1e': 92,          # %
        'Mef2e': 95,          # %
        'SP_Cu': 30,          # g/l
        'SP_Ac': 190,         # g/l
        'AD_Cu': 50,          # g/l
        'Mef1s': 98           # %
    }

    initial_guess_option1 = [10.0]  # Initial v/v%
    bounds_option1 = [(5.0, 30.0)]  # Reasonable bounds for v/v%

    result_option1 = solver.solve_option1(
        config_A.option1_objective,
        initial_guess_option1,
        bounds_option1,
        params_option1
    )

    if result_option1['success']:
        print(f"Optimum v/v%: {result_option1['v_v_percent']:.2f}%")
        print(f"Objective value: {result_option1['objective_value']:.6f}")
    else:
        print("Optimization failed:", result_option1['message'])

    # Test Option 2 - Plant metallurgist mode
    print("\nOption 2 - Plant Metallurgist Mode")

    params_option2 = {
        'PLS_flow': 400,
        'PLS_Cu': 2.5,
        'PLS_Ac': 1.6,
        'O_A_Ext': 1,
        'ML_plant': 4.386,    # From plant lab
        'SP_Cu': 30,
        'SP_Ac': 190,
        'AD_Cu': 50,
        'Mef1s': 98,
        'raffinate_Cu_target': 0.28,
        'stripped_organic_Cu_target': 1.8
    }

    initial_guess_option2 = [8.0, 90.0, 90.0, 95.0]  # [v/v%, SR, Mef1e, Mef2e]
    bounds_option2 = [
        (5.0, 30.0),   # v/v%
        (70.0, 100.0), # SR
        (70.0, 100.0), # Mef1e
        (70.0, 100.0)  # Mef2e
    ]

    result_option2 = solver.solve_option2(
        config_A.option2_objective,
        initial_guess_option2,
        bounds_option2,
        params_option2
    )

    if result_option2['success']:
        print(f"Plant Parameters Found:")
        print(f"  v/v%: {result_option2['v_v_percent']:.2f}%")
        print(f"  Saturation Ratio: {result_option2['saturation_ratio']:.2f}%")
        print(f"  Mixer Efficiency E1: {result_option2['mixer_eff1']:.2f}%")
        print(f"  Mixer Efficiency E2: {result_option2['mixer_eff2']:.2f}%")
        print(f"  Objective value: {result_option2['objective_value']:.6f}")
    else:
        print("Optimization failed:", result_option2['message'])

    # Demonstrate additional calculations
    print("\nAdditional Calculations:")
    v_v_test = 8.66
    aml = sim_engine.calculate_AML(v_v_test)
    print(f"AML for {v_v_test}% extractant: {aml:.3f} g/l Cu")

    # Extraction recovery example
    PLS_Cu = 2.5
    raffinate_Cu = 0.28
    recovery = sim_engine.extraction_recovery(PLS_Cu, raffinate_Cu)
    print(f"Extraction recovery: {recovery:.1f}%")

if __name__ == "__main__":
    main()