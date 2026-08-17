from google.adk.runners import Runner
from google.genai.types import Content, Part
from app.services.session_service import session_service
from app.services.logging_service import fetch_logs
from app.services.monitoring_service import get_cpu_utilization
from app.tools.kubernetes_tool import check_kubernetes_status
from app.tools.security_scan_tool import scan_security
import re


def _guess_service_name(message: str) -> str:
    match = re.search(r"([A-Za-z0-9_-]+\s+service)", message, re.IGNORECASE)
    if match:
        return match.group(1)
    return "target-service"


def run_fast_analysis(message: str, service_name: str | None = None) -> dict:
    service_name = service_name or _guess_service_name(message)
    logs = fetch_logs(service_name)
    metrics = get_cpu_utilization(service_name)
    security = scan_security(service_name)
    kubernetes = check_kubernetes_status(service_name)

    result = {
        "mode": "fast",
        "service": service_name,
        "summary": "Likely infrastructure saturation or OOMKill pattern with no direct security threat detected.",
        "signals": {
            "logs": logs[:3],
            "metrics": metrics,
            "security": security,
            "kubernetes": kubernetes,
        },
        "recommended_next_steps": [
            "Check pod memory limits and recent deploys",
            "Scale the service temporarily if traffic is high",
            "Inspect database or downstream dependency timeouts",
        ],
    }

    return result


def simple_local_model(message: str, service_name: str | None = None) -> str:
    """
    Lightweight local generator that composes a short answer using mock tools.
    This is free and deterministic (no external LLM calls).
    """
    svc = service_name or _guess_service_name(message)
    logs = fetch_logs(svc)
    metrics = get_cpu_utilization(svc)
    security = scan_security(svc)
    kube = check_kubernetes_status(svc)

    parts = []
    parts.append(f"Quick analysis for {svc}:")
    parts.append(f"Summary: Likely {kube['status']} affecting pods; recent logs show {logs[0] if logs else 'no recent errors'}.")
    parts.append(f"Metrics: CPU {metrics.get('cpu_usage')}, Memory {metrics.get('memory_usage')}, Latency {metrics.get('network_latency')}")
    parts.append(f"Security: threat_detected={security.get('threat_detected')}, failed_logins={security.get('failed_logins')}")
    parts.append("Recommended next steps: check pod memory limits, scale temporarily, inspect DB timeouts.")

    return "\n".join(parts)


async def run_agent(agent, user_id: str, message: str, fast_mode: bool = False, service_name: str | None = None, use_simple_model: bool = False):
    # Fast deterministic tool-only path
    if fast_mode:
        return run_fast_analysis(message, service_name=service_name)

    # Simple local model (free) — lightweight text generator using tools
    if use_simple_model:
        return simple_local_model(message, service_name=service_name)

    session = await session_service.create_session(
        app_name=agent.name,
        user_id=user_id
    )

    runner = Runner(
        agent=agent,
        session_service=session_service,
        app_name=agent.name
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=Content(
            parts=[Part(text=message)],
            role="user"
        )
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    return final_response
