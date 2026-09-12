from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
import threading
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.edge_demo import edge_store
from app.services.runner_service import run_agent
from app.services.action_executor import approve_action, reject_action, submit_action
from app.services.incident_service import incident_store

BASE_DIR = Path(__file__).resolve().parent
UI_FILE = BASE_DIR / "ui" / "index.html"
UI_DIR = BASE_DIR / "ui"

app = FastAPI(
    title="CloudGuardian Edge",
    description="Privacy-Preserving On-Device AI Incident Response Platform",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Background auto-tick (every 2 s) ─────────────────────────────────────────
def _auto_ticker():
    while True:
        try:
            edge_store.tick()
        except Exception:
            pass
        time.sleep(2)

_ticker_thread = threading.Thread(target=_auto_ticker, daemon=True)
_ticker_thread.start()


class AnalyzeRequest(BaseModel):
    user_id: str
    workflow: str
    message: str
    service_name: str | None = None
    fast_mode: bool = True
    use_simple_model: bool = False


class ActionDecision(BaseModel):
    operator: str = "operator"


class BenchmarkRequest(BaseModel):
    runs: int = 12


class ScenarioRequest(BaseModel):
    scenario: str = "database_pool"


@app.get("/ui")
@app.get("/")
def ui():
    if not UI_FILE.exists():
        raise HTTPException(status_code=500, detail="UI file not found")
    return FileResponse(UI_FILE, media_type="text/html")


@app.get("/api/stream")
async def sse_stream(request: Request):
    """Server-Sent Events endpoint for real-time dashboard updates."""
    async def event_generator():
        last_tick = 0
        while True:
            if await request.is_disconnected():
                break
            current = edge_store.tick_count
            if current != last_tick:
                last_tick = current
                payload = edge_store.dashboard()
                payload["logs_recent"] = edge_store.logs[-20:]
                yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(0.5)
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/ping")
def health():
    return {"status": "ok", "product": "CloudGuardian Edge", "mode": "LOCAL AI DEMO MODE", "offline_ready": True}


@app.get("/api/health")
def api_health():
    return {
        "status": "ok",
        "version": "2.0.0",
        "mode": "LOCAL AI DEMO MODE",
        "ai_provider": edge_store.ai_provider.name,
        "offline_ready": True,
    }


@app.get("/api/dashboard")
def dashboard():
    return edge_store.dashboard()


@app.post("/api/simulation/tick")
def simulation_tick():
    return edge_store.tick()


@app.get("/api/scenarios")
def scenarios():
    return {
        "scenarios": [
            {"id": "database_pool", "name": "Database Connection Pool Exhaustion"},
            {"id": "payment_latency", "name": "Payment API Latency Spike"},
            {"id": "auth_failures", "name": "Authentication Failure Spike"},
            {"id": "memory_leak", "name": "Memory Leak"},
            {"id": "crash_loop", "name": "Container Crash Loop"},
            {"id": "cpu_saturation", "name": "CPU Saturation"},
            {"id": "cache_failure", "name": "Redis/Cache Failure"},
            {"id": "network_timeout", "name": "Network Timeout Cascade"},
        ]
    }


@app.post("/api/simulation/start")
def simulation_start(request: ScenarioRequest | None = None):
    return edge_store.start_scenario((request.scenario if request else "database_pool"))


@app.post("/api/simulation/stop")
def simulation_stop():
    return edge_store.stop_scenario()


@app.get("/api/services")
def services():
    return {"services": edge_store.services}


@app.get("/api/services/{service_id}")
def service_detail(service_id: str):
    service = next((item for item in edge_store.services if item["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return {
        "service": service,
        "metrics": edge_store.list_by_service(service_id, edge_store.metrics),
        "logs": edge_store.list_by_service(service_id, edge_store.logs),
        "incidents": [item for item in edge_store.incidents if item["serviceId"] == service_id],
        "analyses": [item for item in edge_store.analyses if next((inc for inc in edge_store.incidents if inc["id"] == item["incident"] and inc["serviceId"] == service_id), None)],
    }


@app.get("/api/incidents")
def edge_incidents(
    severity: str | None = None,
    status: str | None = None,
    service: str | None = None,
    search: str | None = None,
):
    incidents = edge_store.incidents
    if severity:
        incidents = [item for item in incidents if item["severity"] == severity.upper()]
    if status:
        incidents = [item for item in incidents if item["status"] == status.upper()]
    if service:
        incidents = [item for item in incidents if item["serviceId"] == service or item["service"] == service]
    if search:
        needle = search.lower()
        incidents = [item for item in incidents if needle in item["title"].lower() or needle in item["summary"].lower()]
    return {"incidents": incidents}


@app.get("/api/incidents/{incident_id}")
def edge_incident_detail(incident_id: str):
    incident = edge_store.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.post("/api/incidents/{incident_id}/analyze")
def edge_analyze_incident(incident_id: str):
    try:
        return edge_store.analyze_incident(incident_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Incident not found")


@app.post("/api/incidents/simulate")
def simulate_incident():
    return edge_store.simulate_incident()


@app.get("/api/logs")
def logs(service: str | None = None, level: str | None = None, severity: str | None = None):
    rows = edge_store.logs
    if service:
        rows = [item for item in rows if item["serviceId"] == service or item["service"] == service]
    if level:
        rows = [item for item in rows if item["level"] == level.upper()]
    if severity:
        rows = [item for item in rows if item["severity"] == severity.upper()]
    return {"logs": rows}


@app.get("/api/metrics")
def metrics(service: str | None = None):
    rows = edge_store.metrics if not service else edge_store.list_by_service(service, edge_store.metrics)
    return {"metrics": rows}


@app.get("/api/remediations")
def remediations():
    return {"remediations": edge_store.remediations}


@app.post("/api/remediations/{remediation_id}/execute")
def execute_remediation(remediation_id: str):
    try:
        return edge_store.execute_remediation(remediation_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Remediation not found")


@app.get("/api/model/performance")
def model_performance():
    return {"provider": edge_store.ai_provider.name, "mode": "LOCAL AI DEMO MODE", "performance": edge_store.performance}


@app.post("/api/model/benchmark")
def benchmark(request: BenchmarkRequest | None = None):
    return edge_store.benchmark((request.runs if request else 12))


@app.get("/api/ai/analyses")
def ai_analyses():
    return {"mode": "LOCAL AI DEMO MODE", "status": "Ready", "offline": True, "model": edge_store.ai_provider.name, "analyses": edge_store.analyses}


@app.post("/api/demo/reset")
def reset_demo():
    return edge_store.reset()


@app.post("/api/demo/seed")
def seed_demo():
    return edge_store.reset()


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    if request.workflow not in {"incident", "remediation"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid workflow. Choose from: ['incident', 'remediation']"
        )

    agent = None
    if not request.fast_mode and not request.use_simple_model:
        try:
            if request.workflow == "incident":
                from app.workflows.incident_workflow import incident_workflow
                agent = incident_workflow
            else:
                from app.workflows.remediation_loop import remediation_loop
                agent = remediation_loop
        except ModuleNotFoundError as error:
            if error.name and error.name.startswith("google.adk"):
                raise HTTPException(
                    status_code=503,
                    detail="Google ADK is not installed. Use fast mode or install the optional AI dependencies."
                ) from error
            raise

    response = await run_agent(
        agent=agent,
        user_id=request.user_id,
        message=request.message,
        fast_mode=request.fast_mode,
        service_name=request.service_name,
        use_simple_model=request.use_simple_model
    )

    if isinstance(response, dict):
        incident = incident_store.create_incident(
            user_id=request.user_id,
            service=response.get("service", request.service_name or "target-service"),
            message=request.message,
            analysis=response,
        )
        action_records = [
            submit_action(incident["id"], action)
            for action in response.get("action_plan", {}).get("actions", [])
        ]
        return {
            "status": "success",
            "workflow": request.workflow,
            "user_id": request.user_id,
            "incident_id": incident["id"],
            "actions": action_records,
            **response,
        }

    return {
        "status": "success",
        "workflow": request.workflow,
        "user_id": request.user_id,
        "response": response
    }


@app.get("/incidents")
def list_incidents():
    return {"incidents": incident_store.list_incidents()}


@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str):
    incident = incident_store.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.get("/pending_actions")
def list_pending_actions():
    return {"actions": incident_store.list_pending_actions()}


@app.post("/actions/{action_id}/approve")
def approve_pending_action(action_id: str, decision: ActionDecision):
    try:
        return approve_action(action_id, decision.operator)
    except KeyError:
        raise HTTPException(status_code=404, detail="Action not found")
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


@app.post("/actions/{action_id}/reject")
def reject_pending_action(action_id: str, decision: ActionDecision):
    try:
        return reject_action(action_id, decision.operator)
    except KeyError:
        raise HTTPException(status_code=404, detail="Action not found")
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
