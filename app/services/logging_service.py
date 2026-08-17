def fetch_logs(service_name: str):
    return [
        f"{service_name} returned 503 error",
        "Database connection timeout after 30s",
        "Pod restarted 5 times in last 10 minutes",
        "Memory limit exceeded on container",
        "Health check endpoint returning 500"
    ]
