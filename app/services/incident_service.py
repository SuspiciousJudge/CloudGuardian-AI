from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class IncidentStore:
    """Small in-memory store used until a durable repository is configured."""

    def __init__(self) -> None:
        self._incidents: dict[str, dict] = {}
        self._actions: dict[str, dict] = {}
        self._lock = Lock()

    def create_incident(self, *, user_id: str, service: str, message: str, analysis: dict) -> dict:
        incident_id = f"inc_{uuid4().hex[:10]}"
        incident = {
            "id": incident_id,
            "user_id": user_id,
            "service": service,
            "message": message,
            "status": "pending_action" if analysis.get("action_plan", {}).get("actions") else "resolved",
            "created_at": _now(),
            "updated_at": _now(),
            "analysis": deepcopy(analysis),
        }
        with self._lock:
            self._incidents[incident_id] = incident
        return deepcopy(incident)

    def list_incidents(self) -> list[dict]:
        with self._lock:
            incidents = list(self._incidents.values())
        return deepcopy(sorted(incidents, key=lambda item: item["created_at"], reverse=True))

    def get_incident(self, incident_id: str) -> dict | None:
        with self._lock:
            incident = self._incidents.get(incident_id)
        return deepcopy(incident) if incident else None

    def create_action(self, incident_id: str, action: dict, status: str) -> dict:
        action_id = f"act_{uuid4().hex[:10]}"
        record = {
            "id": action_id,
            "incident_id": incident_id,
            "action": deepcopy(action),
            "status": status,
            "created_at": _now(),
            "updated_at": _now(),
            "result": None,
        }
        with self._lock:
            self._actions[action_id] = record
        return deepcopy(record)

    def list_pending_actions(self) -> list[dict]:
        with self._lock:
            actions = [item for item in self._actions.values() if item["status"] == "pending_approval"]
        return deepcopy(sorted(actions, key=lambda item: item["created_at"], reverse=True))

    def get_action(self, action_id: str) -> dict | None:
        with self._lock:
            action = self._actions.get(action_id)
        return deepcopy(action) if action else None

    def update_action(self, action_id: str, *, status: str, result: dict | None = None) -> dict:
        with self._lock:
            record = self._actions[action_id]
            record.update({"status": status, "updated_at": _now(), "result": result})
            if status == "executed":
                incident = self._incidents.get(record["incident_id"])
                if incident:
                    incident["status"] = "monitoring"
                    incident["updated_at"] = _now()
            return deepcopy(record)

    def update_incident_status(self, incident_id: str, status: str) -> dict:
        with self._lock:
            incident = self._incidents[incident_id]
            incident.update({"status": status, "updated_at": _now()})
            return deepcopy(incident)


incident_store = IncidentStore()