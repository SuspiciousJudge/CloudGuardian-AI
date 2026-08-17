from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.runner_service import run_agent
from app.workflows.incident_workflow import incident_workflow
from app.workflows.remediation_loop import remediation_loop

BASE_DIR = Path(__file__).resolve().parent
UI_FILE = BASE_DIR / "ui" / "index.html"

app = FastAPI(
    title="CloudGuardian AI",
    description="Enterprise AI Incident Response Platform",
    version="1.0.0"
)


class AnalyzeRequest(BaseModel):
    user_id: str
    workflow: str
    message: str
    service_name: str | None = None
    fast_mode: bool = True
    use_simple_model: bool = False


@app.get("/ui")
def ui():
    if not UI_FILE.exists():
        raise HTTPException(status_code=500, detail="UI file not found")
    return FileResponse(UI_FILE)


@app.get("/")
def health():
    return {
        "status": "CloudGuardian AI is running",
        "version": "1.0.0",
        "workflows": ["incident", "remediation"]
    }


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):

    workflow_map = {
        "incident": incident_workflow,
        "remediation": remediation_loop
    }

    if request.workflow not in workflow_map:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid workflow. Choose from: {list(workflow_map.keys())}"
        )

    agent = workflow_map[request.workflow]

    response = await run_agent(
        agent=agent,
        user_id=request.user_id,
        message=request.message,
        fast_mode=request.fast_mode,
        service_name=request.service_name,
        use_simple_model=request.use_simple_model
    )

    if isinstance(response, dict):
        return {
            "status": "success",
            "workflow": request.workflow,
            "user_id": request.user_id,
            **response,
        }

    return {
        "status": "success",
        "workflow": request.workflow,
        "user_id": request.user_id,
        "response": response
    }
