def scan_security(service_name: str) -> dict:
    """
    Scans for security threats and suspicious activity for a service.
    Returns threat status and failed login attempts.
    """
    return {
        "service": service_name,
        "threat_detected": False,
        "failed_logins": 3,
        "suspicious_ips": ["192.168.1.45"],
        "suspicious_activity": "Multiple failed login attempts detected"
    }
