def check_kubernetes_status(service_name: str) -> dict:
    """
    Checks Kubernetes pod and deployment status for a given service.
    Returns pod health, restart count, and namespace info.
    """
    return {
        "pod_name": f"{service_name}-pod-7d9f8b",
        "status": "CrashLoopBackOff",
        "restart_count": 5,
        "namespace": "production",
        "last_exit_code": 137,
        "reason": "OOMKilled - container exceeded memory limit"
    }
