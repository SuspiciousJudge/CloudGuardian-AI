from app.services.monitoring_service import get_cpu_utilization


def check_infra(service_name: str) -> dict:
    """
    Checks infrastructure health metrics for a given service.
    Returns CPU, memory, and network stats.
    """
    metrics = get_cpu_utilization(service_name)
    return {
        "service": service_name,
        "cpu_usage": metrics["cpu_usage"],
        "memory_usage": metrics["memory_usage"],
        "network_latency": metrics["network_latency"]
    }
