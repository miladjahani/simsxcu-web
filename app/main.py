from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Dict, List

# Import the new simulation and solver engines
from .simulation_engine import SimSXCu, ConfigurationA_2Ex1S, SolverEngine

# --- API Data Models ---

class DesignerParams(BaseModel):
    PLS_flow: float = Field(400, title="PLS Flow", description="m³/h")
    PLS_Cu: float = Field(2.5, title="PLS Copper Concentration", description="g/L")
    PLS_Ac: float = Field(1.6, title="PLS Acidity", description="g/L")
    SR: float = Field(92, title="Saturation Ratio", description="%")
    O_A_Ext: float = Field(1, title="O/A Ratio in Extraction")
    Mef1e: float = Field(92, title="Mixer Efficiency E1", description="%")
    Mef2e: float = Field(95, title="Mixer Efficiency E2", description="%")
    SP_Cu: float = Field(30, title="Spent Electrolyte Copper", description="g/L")
    SP_Ac: float = Field(190, title="Spent Electrolyte Acidity", description="g/L")
    AD_Cu: float = Field(50, title="Advanced Electrolyte Copper", description="g/L")
    Mef1s: float = Field(98, title="Mixer Efficiency S1", description="%")
    initial_vv_guess: float = Field(10.0, title="Initial Guess for v/v %")

class MetallurgistParams(BaseModel):
    PLS_flow: float = Field(400)
    PLS_Cu: float = Field(2.5)
    PLS_Ac: float = Field(1.6)
    O_A_Ext: float = Field(1)
    ML_plant: float = Field(4.386, title="Maximum Loaded from Plant Lab")
    SP_Cu: float = Field(30)
    SP_Ac: float = Field(190)
    AD_Cu: float = Field(50)
    Mef1s: float = Field(98)
    raffinate_Cu_target: float = Field(0.28)
    stripped_organic_Cu_target: float = Field(1.8)
    initial_guess_vv: float = Field(8.0)
    initial_guess_sr: float = Field(90.0)
    initial_guess_mef1e: float = Field(90.0)
    initial_guess_mef2e: float = Field(95.0)

class SolveRequest(BaseModel):
    mode: str = Field(..., description="Either 'designer' or 'metallurgist'")
    params: Dict


# --- FastAPI Application Setup ---

app = FastAPI(
    title="SimSXCu Simulation Engine v2.0",
    description="A web-based simulation tool using the full SimSXCu engine.",
    version="2.0.0"
)

# Mount the static directory to serve frontend files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def read_index():
    """Serves the main index.html file."""
    return FileResponse('app/static/index.html')


@app.post("/api/v1/solve")
async def solve_simulation(request: SolveRequest):
    """
    Main solver endpoint. Instantiates engines and runs the optimization
    based on the selected mode.
    """
    try:
        # Initialize the core engines
        sim_engine = SimSXCu()
        # For now, we only have Configuration A implemented
        config = ConfigurationA_2Ex1S(sim_engine)
        solver = SolverEngine()

        if request.mode == 'designer':
            validated_params = DesignerParams(**request.params)
            initial_guess = [validated_params.initial_vv_guess]
            bounds = [(5.0, 30.0)]  # v/v % bounds

            result = solver.solve_option1(
                config.option1_objective,
                initial_guess,
                bounds,
                validated_params.dict()
            )
            return result

        elif request.mode == 'metallurgist':
            validated_params = MetallurgistParams(**request.params)
            initial_guess = [
                validated_params.initial_guess_vv,
                validated_params.initial_guess_sr,
                validated_params.initial_guess_mef1e,
                validated_params.initial_guess_mef2e
            ]
            bounds = [
                (5.0, 30.0),   # v/v%
                (70.0, 100.0), # SR
                (70.0, 100.0), # Mef1e
                (70.0, 100.0)  # Mef2e
            ]

            result = solver.solve_option2(
                config.option2_objective,
                initial_guess,
                bounds,
                validated_params.dict()
            )
            return result

        else:
            raise HTTPException(status_code=400, detail="Invalid mode specified. Must be 'designer' or 'metallurgist'.")

    except Exception as e:
        # Catch any other errors during simulation
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")