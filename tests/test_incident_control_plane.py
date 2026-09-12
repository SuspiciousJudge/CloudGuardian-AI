from app.services import action_executor
from app.services.incident_service import IncidentStore


def make_incident(store: IncidentStore) -> str:
    incident = store.create_incident(
        user_id="operator",
        service="payment-service",
        message="Payment service is failing",
        analysis={"action_plan": {"actions": []}},
    )
    return incident["id"]


def test_pending_action_can_be_approved(monkeypatch):
    store = IncidentStore()
    monkeypatch.setattr(action_executor, "incident_store", store)
    monkeypatch.setattr(action_executor, "AUTOMATION_ENABLED", False)

    incident_id = make_incident(store)
    action = {
        "type": "restart_service",
        "parameters": {"service": "payment-service"},
        "risk_level": "low",
        "description": "Restart the service",
    }

    pending = action_executor.submit_action(incident_id, action)
    approved = action_executor.approve_action(pending["id"], "operator")

    assert pending["status"] == "pending_approval"
    assert approved["status"] == "executed"
    assert approved["result"]["mode"] == "simulation"
    assert store.get_incident(incident_id)["status"] == "monitoring"


def test_pending_action_can_be_rejected(monkeypatch):
    store = IncidentStore()
    monkeypatch.setattr(action_executor, "incident_store", store)
    monkeypatch.setattr(action_executor, "AUTOMATION_ENABLED", False)

    incident_id = make_incident(store)
    pending = action_executor.submit_action(
        incident_id,
        {"type": "increase_memory", "risk_level": "medium"},
    )
    rejected = action_executor.reject_action(pending["id"], "operator")

    assert rejected["status"] == "rejected"
    assert rejected["result"]["rejected_by"] == "operator"
    assert store.list_pending_actions() == []


def test_automatic_execution_requires_explicit_enablement(monkeypatch):
    store = IncidentStore()
    monkeypatch.setattr(action_executor, "incident_store", store)
    monkeypatch.setattr(action_executor, "AUTOMATION_ENABLED", True)

    incident_id = make_incident(store)
    result = action_executor.submit_action(
        incident_id,
        {
            "type": "restart_service",
            "parameters": {"service": "payment-service"},
            "risk_level": "low",
        },
    )

    assert result["status"] == "executed"
    assert result["result"]["mode"] == "adapter_pending"
    assert store.list_pending_actions() == []