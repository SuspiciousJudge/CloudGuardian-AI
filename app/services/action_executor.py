from __future__ import annotations

import os

from app.services.incident_service import incident_store


AUTOMATIC_ACTIONS = {"restart_service"}
AUTOMATION_ENABLED = os.getenv("CLOUDGUARDIAN_AUTOMATION_ENABLED", "false").lower() == "true"


def _execution_result(action: dict, *, approved_by: str) -> dict:
    """Execute only the non-destructive prototype action; live adapters come later."""
    action_type = action.get("type")
    if action_type == "restart_service":
        return {
            "mode": "simulation" if not AUTOMATION_ENABLED else "adapter_pending",
            "message": f"Restart request accepted for {action.get('parameters', {}).get('service', 'unknown service')}",
            "approved_by": approved_by,
        }
    return {"mode": "blocked", "message": "No executor is registered for this action type."}


def submit_action(incident_id: str, action: dict) -> dict:
    action_type = action.get("type")
    risk_level = action.get("risk_level")
    if risk_level == "low" and action_type in AUTOMATIC_ACTIONS and AUTOMATION_ENABLED:
        record = incident_store.create_action(incident_id, action, "executing")
        result = _execution_result(action, approved_by="system")
        return incident_store.update_action(record["id"], status="executed", result=result)
    return incident_store.create_action(incident_id, action, "pending_approval")


def approve_action(action_id: str, approved_by: str) -> dict:
    record = incident_store.get_action(action_id)
    if not record:
        raise KeyError(action_id)
    if record["status"] != "pending_approval":
        raise ValueError("Only pending actions can be approved")
    result = _execution_result(record["action"], approved_by=approved_by)
    status = "executed" if result["mode"] != "blocked" else "blocked"
    return incident_store.update_action(action_id, status=status, result=result)


def reject_action(action_id: str, rejected_by: str) -> dict:
    record = incident_store.get_action(action_id)
    if not record:
        raise KeyError(action_id)
    if record["status"] != "pending_approval":
        raise ValueError("Only pending actions can be rejected")
    return incident_store.update_action(
        action_id,
        status="rejected",
        result={"message": "Action rejected by operator", "rejected_by": rejected_by},
    )