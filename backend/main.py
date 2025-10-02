from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

from .simulation_engine import SimulationEngine

# --- Pydantic Models for Data Validation ---

class SimulationParameters(BaseModel):
    """
    Defines the input parameters for the simulation.
    Values are based on the original prototype's defaults.
    """
    PLS_flow: float = Field(400, title="PLS Flow", description="m³/h")
    PLS_Cu: float = Field(2.5, title="PLS Copper Concentration", description="g/L")
    PLS_Ac: float = Field(1.6, title="PLS Acidity", description="g/L")
    SR: float = Field(92, title="Saturation Ratio", description="%")
    Ratio_O_A_Ext: float = Field(1, title="Organic/Aqueous Ratio in Extraction")
    Mef1e: float = Field(92, title="Mixer Efficiency E1", description="%")
    Mef2e: float = Field(95, title="Mixer Efficiency E2", description="%")
    SP_Cu: float = Field(30, title="Spent Electrolyte Copper", description="g/L")
    SPAc: float = Field(190, title="Spent Electrolyte Acidity", description="g/L")
    AD_Cu: float = Field(50, title="Advanced Electrolyte Copper", description="g/L")
    Mef1s: float = Field(98, title="Mixer Efficiency S1", description="%")
    v_v_percent: float = Field(8.66, title="Extractant Volume Percentage", description="% v/v")

class SimulationRequest(BaseModel):
    """
    Defines the structure of a simulation API request.
    """
    option: Literal[1, 2] = Field(..., title="Simulation Option", description="Option 1 or Option 2")
    config: str = Field("A", title="Plant Configuration", description="e.g., 'A', 'B', etc.")
    parameters: SimulationParameters


# --- FastAPI Application ---

app = FastAPI(
    title="SimSXCu Simulation Engine API",
    description="A smart, interactive web-based simulation tool for copper solvent extraction.",
    version="1.0.0"
)

engine = SimulationEngine()

@app.get("/")
async def root():
    """Root endpoint providing a welcome message."""
    return {"message": "Welcome to the SimSXCu Simulation Engine API"}

@app.post("/api/v1/simulate")
async def run_simulation(request: SimulationRequest):
    """
    Runs a simulation based on the provided configuration, option, and parameters.
    - Option 1: Optimizes for minimum extractant (v/v %) for a target recovery.
    - Option 2: Simulates plant performance with a given extractant (v/v %).
    """
    params_dict = request.parameters.model_dump()

    if request.option == 1:
        # Call the new optimization method from the solver-based engine
        results = engine.run_optimization(params_dict)
    else:  # Option 2
        # Call the new direct simulation method
        results = engine.run_simulation(params_dict)

    return {"results": results}