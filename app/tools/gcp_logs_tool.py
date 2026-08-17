from app.services.logging_service import fetch_logs


def analyze_logs(service_name: str) -> dict:
    """
    Fetches and analyzes production logs for a given service.
    Returns error summary and log details.
    """
    logs = fetch_logs(service_name)
    return {
        "service": service_name,
        "total_errors": len(logs),
        "logs": logs
    }
