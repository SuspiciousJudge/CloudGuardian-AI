import pytest
from fastapi import HTTPException

from app.main import (
    BenchmarkRequest,
    api_health,
    benchmark,
    dashboard,
    edge_analyze_incident,
    edge_incident_detail,
    execute_remediation,
    logs,
    remediations,
    reset_demo,
    simulate_incident,
)


def test_health_dashboard_and_mock_data():
    assert api_health()["mode"] == "LOCAL AI DEMO MODE"
    data = dashboard()
    assert data["cards"]["totalServices"] == 8
    assert len(data["services"]) == 8
    assert len(data["metrics"]) >= 50
    assert len(logs()["logs"]) >= 30
    assert len(data["incidents"]) >= 8


def test_simulate_analyze_remediate_benchmark_and_reset():
    simulated = simulate_incident()
    incident = simulated["incident"]
    assert incident["id"] == "inc-demo-db-pool"
    assert incident["status"] == "ACTIVE"
    assert simulated["analysis"]["rootCause"] == "Database connection pool exhausted due to connection saturation."

    detail = edge_incident_detail(incident["id"])
    assert detail["analysis"]["confidence"] == 94
    assert detail["logs"]

    remediation = next(item for item in remediations()["remediations"] if item["incidentId"] == incident["id"])
    executed = execute_remediation(remediation["id"])
    assert executed["status"] == "Executed"

    result = benchmark(BenchmarkRequest(runs=5))
    assert result["runs"] == 5
    assert result["averageLatencyMs"] >= 0

    assert reset_demo()["status"] == "reset"
    assert dashboard()["cards"]["healthyServices"] == 8


def test_invalid_ids_raise_404():
    with pytest.raises(HTTPException) as incident_error:
        edge_incident_detail("missing")
    assert incident_error.value.status_code == 404

    with pytest.raises(HTTPException) as analyze_error:
        edge_analyze_incident("missing")
    assert analyze_error.value.status_code == 404

    with pytest.raises(HTTPException) as remediation_error:
        execute_remediation("missing")
    assert remediation_error.value.status_code == 404
