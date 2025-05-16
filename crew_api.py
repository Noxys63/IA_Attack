from fastapi import FastAPI
from pydantic import BaseModel
from crew_attack_simulation import run_phase1, run_phase2

app = FastAPI()

class PhaseResponse(BaseModel):
    message: str
    result: str

@app.get("/")
def index():
    return {"message": "CrewAI Simulation API is running!"}

@app.post("/run/phase1", response_model=PhaseResponse)
def launch_phase1():
    result = run_phase1()
    return {"message": "Phase 1 exécutée avec succès", "result": result}

@app.post("/run/phase2", response_model=PhaseResponse)
def launch_phase2():
    result = run_phase2()
    return {"message": "Phase 2 exécutée avec succès", "result": result}
