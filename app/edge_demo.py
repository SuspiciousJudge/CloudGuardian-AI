from __future__ import annotations

import statistics
import time
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from threading import Lock


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def iso(minutes_ago: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat()


class AIProvider:
    name = "AIProvider"
    mode = "abstract"

    def analyze(self, incident: dict, logs: list[dict], metrics: list[dict]) -> dict:
        raise NotImplementedError


class LocalAIProvider(AIProvider):
    name = "Local Demo Analyzer"
    mode = "local_demo"

    def analyze(self, incident: dict, logs: list[dict], metrics: list[dict]) -> dict:
        start = time.perf_counter()
        text = " ".join([incident.get("title", ""), incident.get("summary", "")] + [log["message"] for log in logs]).lower()
        latest = metrics[-1] if metrics else {}
        evidence = []
        if latest.get("dbConnections", 0) >= 90:
            evidence.append(f"Database connections reached {latest.get('dbConnections')}/100")
        if latest.get("latency", 0) >= 500:
            evidence.append(f"{incident.get('service', 'Service')} latency exceeded {latest.get('latency')}ms")
        if latest.get("errorRate", 0) >= 5:
            evidence.append(f"Error rate rose to {latest.get('errorRate')}%")
        if any("timeout" in log["message"].lower() or "connection" in log["message"].lower() for log in logs):
            evidence.append("Recent logs contain timeout or connection acquisition failures")
        if "connection pool" in text or latest.get("dbConnections", 0) >= 90:
            root = "Database connection pool exhausted due to connection saturation."
            factors = [
                "Database connection utilization exceeded 90%",
                "Payment API latency rose after database saturation",
                "Error logs show checkout requests waiting for database connections",
            ]
            actions = [
                {"id": "rem-db-pool", "action": "Increase DB Connection Pool", "risk": "Low", "expectedImpact": "High", "status": "Recommended"},
                {"id": "rem-stale-connections", "action": "Terminate stale connections", "risk": "Medium", "expectedImpact": "High", "status": "Recommended"},
                {"id": "rem-worker-restart", "action": "Restart affected workers", "risk": "Medium", "expectedImpact": "Medium", "status": "Recommended"},
                {"id": "rem-pool-monitoring", "action": "Enable connection pool monitoring", "risk": "Low", "expectedImpact": "Medium", "status": "Recommended"},
            ]
            confidence = 82 + min(12.2, len(evidence) * 3.05)
        elif latest.get("cpu", 0) > 85:
            root = "Compute saturation is the probable cause of degraded service health."
            factors = ["CPU utilization exceeded the service threshold", "Request queue depth increased", "Latency moved with CPU pressure"]
            actions = [{"id": "rem-scale", "action": "Scale service replicas", "risk": "Low", "expectedImpact": "High", "status": "Recommended"}]
            confidence = 80 + min(10.5, len(evidence) * 2.5)
        else:
            root = "Telemetry indicates a localized service degradation with no cloud dependency required for analysis."
            factors = ["Recent warning logs correlate with elevated latency", "Error rate is above normal baseline"]
            actions = [{"id": "rem-observe", "action": "Continue local monitoring", "risk": "Low", "expectedImpact": "Medium", "status": "Recommended"}]
            confidence = 78 + min(8, len(evidence) * 2)
        latency_ms = round((time.perf_counter() - start) * 1000, 3)
        return {
            "incident": incident["id"],
            "severity": incident["severity"],
            "rootCause": root,
            "confidence": round(confidence, 1),
            "contributingFactors": factors,
            "evidence": evidence or ["Telemetry crossed local anomaly thresholds"],
            "recommendedActions": actions,
            "explanation": "Local AI Demo Mode uses deterministic telemetry reasoning over logs, metrics, and incident metadata. It does not call a cloud AI API.",
            "latencyMs": latency_ms,
            "timestamp": now_iso(),
            "model": self.name,
            "mode": self.mode,
        }


class CloudAIProvider(AIProvider):
    name = "Cloud Provider Adapter"
    mode = "cloud_adapter"

    def analyze(self, incident: dict, logs: list[dict], metrics: list[dict]) -> dict:
        raise RuntimeError("Cloud AI provider is intentionally disabled for localhost demo mode.")


class EdgeDemoStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self.ai_provider: AIProvider = LocalAIProvider()
        self.reset()

    def reset(self) -> dict:
        with self._lock:
            self.tick_count = 0
            self.scenario = {"name": None, "state": "HEALTHY", "phase": "BASELINE", "startedAt": None, "ticks": 0, "selected": "database_pool"}
            self.services = self._seed_services()
            self.metrics = self._seed_metrics()
            self.logs = self._seed_logs()
            self.incidents = self._seed_incidents()
            self.analyses: list[dict] = []
            self.remediations = self._seed_remediations()
            self.performance = {"runs": 0, "averageLatencyMs": None, "minimumLatencyMs": None, "maximumLatencyMs": None, "throughputPerSecond": None, "modelSize": "Not measured", "memoryUsage": "Not measured", "accuracy": "Not measured", "updatedAt": None}
            self.activity = [
                {"timestamp": iso(6), "event": "Local AI Demo Mode ready"},
                {"timestamp": iso(5), "event": "Mock telemetry seeded"},
                {"timestamp": iso(4), "event": "System healthy"},
            ]
        return {"status": "reset", "message": "Demo data restored to deterministic healthy baseline"}

    def _seed_services(self) -> list[dict]:
        names = ["API Gateway", "Authentication Service", "User Service", "Payment Service", "Order Service", "Notification Service", "Database Service", "Background Worker"]
        versions = ["v3.1.0", "v2.7.4", "v2.2.9", "v2.4.1", "v1.9.8", "v2.0.6", "v14.7.2", "v1.6.3"]
        return [{"id": f"svc-{i+1}", "name": name, "status": "HEALTHY", "cpu": 32 + i * 3, "memory": 45 + i * 2, "latency": 88 + i * 9, "errorRate": round(0.18 + i * 0.04, 2), "requestsPerSecond": 1240 - i * 95, "requestsPerSec": 1240 - i * 95, "activeConnections": 35 + i, "uptime": round(99.99 - i * 0.01, 2), "version": versions[i], "region": "us-east-1", "lastUpdated": now_iso()} for i, name in enumerate(names)]

    def _seed_metrics(self) -> list[dict]:
        rows = []
        for svc in self.services:
            for i in range(7):
                rows.append({"id": f"met-{svc['id']}-{i}", "serviceId": svc["id"], "timestamp": iso(120 - i * 4), "cpu": svc["cpu"] + (i % 3), "memory": svc["memory"] + (i % 4), "latency": svc["latency"] + i * 2, "errorRate": svc["errorRate"], "requestsPerSecond": svc["requestsPerSecond"] + i * 3, "requestsPerSec": svc["requestsPerSecond"] + i * 3, "activeConnections": svc["activeConnections"] + i, "dbConnections": 38 + i})
        rows.append({"id": "met-global-1", "serviceId": "global", "timestamp": iso(1), "cpu": 42, "memory": 55, "latency": 118, "errorRate": 0.34, "requestsPerSecond": 5840, "requestsPerSec": 5840, "activeConnections": 410, "dbConnections": 44})
        return rows

    def _seed_logs(self) -> list[dict]:
        levels = ["INFO", "WARN", "ERROR", "CRITICAL"]
        messages = [
            "Request completed within latency budget",
            "Cache refresh completed",
            "Connection pool headroom normal",
            "Worker heartbeat acknowledged",
            "Dependency health probe succeeded",
        ]
        logs = []
        for i in range(104):
            svc = self.services[i % len(self.services)]
            level = levels[0 if i < 20 else 1 if i < 26 else 2]
            logs.append({"id": f"log-{i+1}", "timestamp": iso(180 - i), "serviceId": svc["id"], "service": svc["name"], "level": level, "severity": level, "message": messages[i % len(messages)], "requestId": f"req-{10000+i}", "traceId": f"trace-{70000+i}"})
        return logs

    def _seed_incidents(self) -> list[dict]:
        templates = [
            ("inc-001", "Database connection pool exhaustion", "CRITICAL", "Payment Service", "RESOLVED", 94),
            ("inc-002", "API latency spike", "HIGH", "API Gateway", "RESOLVED", 87),
            ("inc-003", "Memory leak", "HIGH", "Background Worker", "MITIGATED", 89),
            ("inc-004", "CPU saturation", "MEDIUM", "Order Service", "RESOLVED", 83),
            ("inc-005", "Authentication failure spike", "HIGH", "Authentication Service", "RESOLVED", 86),
            ("inc-006", "Redis/cache failure", "MEDIUM", "User Service", "MITIGATED", 78),
            ("inc-009", "Network timeout cascade", "HIGH", "API Gateway", "RESOLVED", 84),
            ("inc-010", "Payment timeout", "CRITICAL", "Payment Service", "RESOLVED", 91),
            ("inc-008", "Container crash loop", "LOW", "Notification Service", "RESOLVED", 74),
        ]
        result = []
        for i, (iid, title, sev, service, status, conf) in enumerate(templates):
            svc = next(s for s in self.services if s["name"] == service)
            result.append({"id": iid, "title": title, "severity": sev, "serviceId": svc["id"], "service": service, "status": status, "detectedAt": iso(180 + i * 25), "aiConfidence": conf, "summary": f"{title} detected in {service} telemetry.", "timeline": ["Incident detected", "AI analysis completed", "Remediation recommended", status.title()]})
        return result

    def _seed_remediations(self) -> list[dict]:
        actions = ["Increase DB Connection Pool", "Terminate stale connections", "Restart affected workers", "Enable connection pool monitoring", "Scale API Gateway replicas", "Tune authentication rate limits", "Warm cache cluster", "Increase worker memory", "Adjust payment timeout budget", "Review container probe thresholds"]
        return [{"id": f"rem-{i+1}", "incidentId": self.incidents[i % len(self.incidents)]["id"], "incident": self.incidents[i % len(self.incidents)]["title"], "action": action, "risk": "Low" if i % 3 != 1 else "Medium", "expectedImpact": "High" if i < 5 else "Medium", "status": "Recommended"} for i, action in enumerate(actions)]

    def dashboard(self) -> dict:
        active = [i for i in self.incidents if i["status"] in {"ACTIVE", "INVESTIGATING"}]
        healthy = [s for s in self.services if s["status"] == "HEALTHY"]
        return {"mode": "LOCAL AI DEMO MODE", "offlineReady": True, "simulation": deepcopy(self.scenario), "lastUpdate": now_iso(), "privacy": "No telemetry is sent to a cloud AI API in Local AI Demo Mode.", "cards": {"totalServices": len(self.services), "healthyServices": len(healthy), "activeIncidents": len(active), "criticalIncidents": len([i for i in active if i["severity"] == "CRITICAL"])}, "services": deepcopy(self.services), "incidents": deepcopy(self.incidents), "metrics": deepcopy(self.metrics[-130:]), "activity": deepcopy(self.activity)}

    def tick(self) -> dict:
        with self._lock:
            self.tick_count += 1
            for index, service in enumerate(self.services):
                wave = ((self.tick_count + index) % 6) - 2
                service["cpu"] = max(25, min(65, service["cpu"] + wave))
                service["memory"] = max(40, min(70, service["memory"] + (1 if self.tick_count % 4 == 0 else -1 if self.tick_count % 5 == 0 else 0)))
                service["latency"] = max(80, min(180, service["latency"] + wave * 3))
                service["errorRate"] = round(max(0.1, min(1.0, service["errorRate"] + wave * 0.02)), 2)
                service["requestsPerSecond"] = max(500, service["requestsPerSecond"] + wave * 12)
                service["requestsPerSec"] = service["requestsPerSecond"]
                service["activeConnections"] = max(20, min(85, service["activeConnections"] + wave))
                service["lastUpdated"] = now_iso()
                self.metrics.append(self._metric_for(service))
            if self.scenario["state"] != "HEALTHY":
                self._advance_database_scenario()
            if self.tick_count % 2 == 0:
                self._append_log(self.services[self.tick_count % len(self.services)], "INFO", "request completed")
            self.metrics = self.metrics[-960:]
            self.logs = self.logs[-250:]
        return self.dashboard()

    def _metric_for(self, service: dict) -> dict:
        return {"id": f"met-live-{self.tick_count}-{service['id']}", "serviceId": service["id"], "timestamp": now_iso(), "cpu": service["cpu"], "memory": service["memory"], "latency": service["latency"], "errorRate": service["errorRate"], "requestsPerSecond": service["requestsPerSecond"], "requestsPerSec": service["requestsPerSecond"], "activeConnections": service["activeConnections"], "dbConnections": service["activeConnections"] if service["name"] == "Database Service" else 44}

    def _append_log(self, service: dict, level: str, message: str) -> None:
        self.logs.append({"id": f"log-live-{len(self.logs)+1}", "timestamp": now_iso(), "serviceId": service["id"], "service": service["name"], "level": level, "severity": level, "message": message, "requestId": f"req-{self.tick_count:05d}", "traceId": f"trace-{self.tick_count:05d}"})

    def start_scenario(self, scenario: str = "database_pool") -> dict:
        with self._lock:
            names = {
                "database_pool": "Database Connection Pool Exhaustion",
                "payment_latency": "Payment API Latency Spike",
                "auth_failures": "Authentication Failure Spike",
                "memory_leak": "Memory Leak",
                "crash_loop": "Container Crash Loop",
                "cpu_saturation": "CPU Saturation",
                "cache_failure": "Redis/Cache Failure",
                "network_timeout": "Network Timeout Cascade",
            }
            label = names.get(scenario, scenario)
            self.scenario = {"name": scenario, "label": label, "state": "DEGRADING", "phase": "PHASE 2 - DEGRADATION", "startedAt": now_iso(), "ticks": 0, "selected": scenario}
            self.activity.insert(0, {"timestamp": now_iso(), "event": f"{label} simulation started"})
        return self.dashboard()

    def stop_scenario(self) -> dict:
        with self._lock:
            self.scenario["state"] = "HEALTHY"
            self.scenario["phase"] = "STOPPED"
            self.scenario["ticks"] = 0
        return self.dashboard()

    def _advance_database_scenario(self) -> None:
        # dispatcher
        name = self.scenario.get("name", "database_pool")
        if name == "database_pool":
            self._scenario_db_pool()
        elif name == "payment_latency":
            self._scenario_payment_latency()
        elif name == "auth_failures":
            self._scenario_auth_failures()
        elif name == "memory_leak":
            self._scenario_memory_leak()
        elif name == "crash_loop":
            self._scenario_crash_loop()
        elif name == "cpu_saturation":
            self._scenario_cpu_saturation()
        elif name == "cache_failure":
            self._scenario_cache_failure()
        elif name == "network_timeout":
            self._scenario_network_timeout()
        else:
            self._scenario_db_pool()

    def _recovery_done(self, svc_name: str, inc_id: str, phase: str = "PHASE 7 - RECOVERED") -> bool:
        """Mark incident mitigated and transition scenario to RECOVERED."""
        svc = next((s for s in self.services if s["name"] == svc_name), None)
        if svc:
            svc["status"] = "HEALTHY"
        incident = next((i for i in self.incidents if i["id"] == inc_id), None)
        if incident:
            incident["status"] = "MITIGATED"
            incident["timeline"].append(f"{now_iso()} Service recovered")
        self.scenario["state"] = "RECOVERED"
        self.scenario["phase"] = phase
        self.activity.insert(0, {"timestamp": now_iso(), "event": f"{svc_name} recovered after remediation"})
        return True

    def _scenario_db_pool(self) -> None:
        self.scenario["ticks"] += 1
        t = self.scenario["ticks"]
        payment = next(s for s in self.services if s["name"] == "Payment Service")
        database = next(s for s in self.services if s["name"] == "Database Service")
        if self.scenario["state"] == "MITIGATING":
            payment["latency"] = max(124, payment["latency"] - 420)
            payment["errorRate"] = round(max(0.3, payment["errorRate"] - 3.5), 2)
            payment["cpu"] = max(41, payment["cpu"] - 8)
            database["activeConnections"] = max(42, database["activeConnections"] - 12)
            database["cpu"] = max(40, database["cpu"] - 7)
            self._append_log(payment, "INFO", "[RECOVERY] Connection pool headroom restored — payment throughput normalizing")
            if payment["latency"] <= 180 and payment["errorRate"] <= 1.0:
                database["status"] = "HEALTHY"
                self._recovery_done("Payment Service", "inc-demo-db-pool")
            return
        db_connections = min(100, 42 + t * 9)
        latency_curve = [120, 180, 300, 800, 1800, 3500]
        error_curve  = [0.3,  1.0,  2.0,  6.0,  12.0, 19.0]
        idx = min(t, len(latency_curve) - 1)
        database.update({"status": "DEGRADED" if t < 5 else "CRITICAL", "activeConnections": db_connections, "cpu": min(96, 45 + t * 7), "lastUpdated": now_iso()})
        payment.update({"status": "DEGRADED" if t < 5 else "CRITICAL", "latency": latency_curve[idx], "errorRate": error_curve[idx], "cpu": min(94, 41 + t * 7), "memory": min(92, 56 + t * 4), "lastUpdated": now_iso()})
        self.metrics.append(self._metric_for(payment))
        self.metrics.append({**self._metric_for(database), "dbConnections": db_connections})
        if t in {1, 2, 3}:
            self._append_log(database, "WARN", f"Connection pool utilization at {db_connections}/100 — approaching threshold")
            self.activity.insert(0, {"timestamp": now_iso(), "event": "Elevated database connections detected"})
        if t >= 4:
            self._append_log(payment, "ERROR", f"[req-{t:05d}] Payment checkout timed out waiting for DB connection (pool={db_connections}/100)")
            self.activity.insert(0, {"timestamp": now_iso(), "event": "Payment API latency threshold exceeded"})
        if t >= 5:
            self._append_log(database, "CRITICAL", "Connection pool EXHAUSTED 100/100 — all workers blocked")
            self._ensure_demo_incident("inc-demo-db-pool", "Database Connection Pool Exhaustion", "CRITICAL", "Payment Service",
                "Payment Service cannot acquire DB connections. Pool fully saturated.")

    def _scenario_payment_latency(self) -> None:
        self.scenario["ticks"] += 1
        t = self.scenario["ticks"]
        payment = next(s for s in self.services if s["name"] == "Payment Service")
        if self.scenario["state"] == "MITIGATING":
            payment["latency"] = max(130, payment["latency"] - 300)
            payment["errorRate"] = round(max(0.4, payment["errorRate"] - 2.0), 2)
            self._append_log(payment, "INFO", "[RECOVERY] Payment gateway latency normalizing")
            if payment["latency"] <= 200:
                self._recovery_done("Payment Service", "inc-demo-pay-lat")
            return
        latency_curve = [130, 250, 600, 1200, 2800, 4800]
        error_curve   = [0.4,  1.5,  4.0,  9.0, 15.0, 22.0]
        idx = min(t, len(latency_curve) - 1)
        payment.update({"status": "DEGRADED" if t < 4 else "CRITICAL", "latency": latency_curve[idx], "errorRate": error_curve[idx], "cpu": min(88, 40 + t * 8), "lastUpdated": now_iso()})
        self.metrics.append(self._metric_for(payment))
        if t in {1, 2}:
            self._append_log(payment, "WARN", f"Payment gateway P99 latency elevated: {latency_curve[idx]}ms (threshold 300ms)")
        if t >= 3:
            self._append_log(payment, "ERROR", f"Payment service timeout — upstream gateway not responding within {latency_curve[idx]}ms")
        if t >= 4:
            self._ensure_demo_incident("inc-demo-pay-lat", "Payment API Latency Spike", "HIGH", "Payment Service",
                "Payment Service upstream gateway timeouts causing cascading failures.")

    def _scenario_auth_failures(self) -> None:
        self.scenario["ticks"] += 1
        t = self.scenario["ticks"]
        auth = next(s for s in self.services if s["name"] == "Authentication Service")
        if self.scenario["state"] == "MITIGATING":
            auth["errorRate"] = round(max(0.2, auth["errorRate"] - 4.0), 2)
            auth["cpu"] = max(35, auth["cpu"] - 10)
            self._append_log(auth, "INFO", "[RECOVERY] Auth rate limits applied — failure rate declining")
            if auth["errorRate"] <= 1.0:
                self._recovery_done("Authentication Service", "inc-demo-auth")
            return
        fail_curve = [0.5, 2.0, 6.0, 14.0, 25.0, 38.0]
        idx = min(t, len(fail_curve) - 1)
        auth.update({"status": "DEGRADED" if t < 4 else "CRITICAL", "errorRate": fail_curve[idx], "cpu": min(92, 35 + t * 9), "lastUpdated": now_iso()})
        self.metrics.append(self._metric_for(auth))
        if t in {1, 2}:
            self._append_log(auth, "WARN", f"Auth failure rate {fail_curve[idx]}% — possible credential stuffing attack")
        if t >= 3:
            self._append_log(auth, "ERROR", f"[req-{t:05d}] JWT validation failures spike: {fail_curve[idx]}% of requests rejected")
        if t >= 4:
            self._ensure_demo_incident("inc-demo-auth", "Authentication Failure Spike", "HIGH", "Authentication Service",
                "Spike in auth failures — possible brute-force or misconfigured token issuer.")

    def _scenario_memory_leak(self) -> None:
        self.scenario["ticks"] += 1
        t = self.scenario["ticks"]
        worker = next(s for s in self.services if s["name"] == "Background Worker")
        if self.scenario["state"] == "MITIGATING":
            worker["memory"] = max(55, worker["memory"] - 8)
            self._append_log(worker, "INFO", "[RECOVERY] Worker GC pressure relieved — heap stabilizing")
            if worker["memory"] <= 65:
                self._recovery_done("Background Worker", "inc-demo-mem-leak")
            return
        mem_curve = [58, 65, 72, 80, 87, 93]
        idx = min(t, len(mem_curve) - 1)
        worker.update({"status": "DEGRADED" if t < 4 else "CRITICAL", "memory": mem_curve[idx], "cpu": min(80, 30 + t * 5), "lastUpdated": now_iso()})
        self.metrics.append(self._metric_for(worker))
        if t in {1, 2, 3}:
            self._append_log(worker, "WARN", f"Heap usage at {mem_curve[idx]}% — GC pause times increasing")
        if t >= 4:
            self._append_log(worker, "ERROR", f"OOM risk: heap {mem_curve[idx]}% — container memory pressure critical")
        if t >= 4:
            self._ensure_demo_incident("inc-demo-mem-leak", "Memory Leak", "HIGH", "Background Worker",
                "Background Worker heap continuously growing — suspected memory leak in job processor.")

    def _scenario_crash_loop(self) -> None:
        self.scenario["ticks"] += 1
        t = self.scenario["ticks"]
        notif = next(s for s in self.services if s["name"] == "Notification Service")
        if self.scenario["state"] == "MITIGATING":
            notif["errorRate"] = round(max(0.3, notif["errorRate"] - 5.0), 2)
            self._append_log(notif, "INFO", "[RECOVERY] Container probe thresholds adjusted — pod stabilizing")
            if notif["errorRate"] <= 1.0:
                self._recovery_done("Notification Service", "inc-demo-crash")
            return
        crash_err = [0.5, 3.0, 8.0, 18.0, 30.0, 45.0]
        idx = min(t, len(crash_err) - 1)
        notif.update({"status": "DEGRADED" if t < 4 else "CRITICAL", "errorRate": crash_err[idx], "lastUpdated": now_iso()})
        self.metrics.append(self._metric_for(notif))
        if t in {1, 2}:
            self._append_log(notif, "WARN", f"Container restart #{t} detected for notification-worker-0")
        if t >= 3:
            self._append_log(notif, "ERROR", f"CrashLoopBackOff: notification-worker-0 restarted {t * 3} times in 5 minutes")
        if t >= 4:
            self._ensure_demo_incident("inc-demo-crash", "Container Crash Loop", "HIGH", "Notification Service",
                "Notification Service pod in CrashLoopBackOff — liveness probe failures causing continuous restarts.")

    def _scenario_cpu_saturation(self) -> None:
        self.scenario["ticks"] += 1
        t = self.scenario["ticks"]
        order = next(s for s in self.services if s["name"] == "Order Service")
        if self.scenario["state"] == "MITIGATING":
            order["cpu"] = max(45, order["cpu"] - 12)
            order["latency"] = max(120, order["latency"] - 200)
            self._append_log(order, "INFO", "[RECOVERY] Additional replicas provisioned — CPU utilization declining")
            if order["cpu"] <= 65:
                self._recovery_done("Order Service", "inc-demo-cpu")
            return
        cpu_curve = [55, 68, 78, 87, 93, 98]
        lat_curve  = [140, 220, 450, 900, 2200, 4500]
        idx = min(t, len(cpu_curve) - 1)
        order.update({"status": "DEGRADED" if t < 4 else "CRITICAL", "cpu": cpu_curve[idx], "latency": lat_curve[idx], "lastUpdated": now_iso()})
        self.metrics.append(self._metric_for(order))
        if t in {1, 2}:
            self._append_log(order, "WARN", f"CPU throttling active on order-service — current: {cpu_curve[idx]}% (limit: 80%)")
        if t >= 3:
            self._append_log(order, "ERROR", f"Order service request queue depth: {t * 180} — CPU saturated at {cpu_curve[idx]}%")
        if t >= 4:
            self._ensure_demo_incident("inc-demo-cpu", "CPU Saturation", "HIGH", "Order Service",
                "Order Service CPU pegged at max — request queue backing up.")

    def _scenario_cache_failure(self) -> None:
        self.scenario["ticks"] += 1
        t = self.scenario["ticks"]
        user_svc = next(s for s in self.services if s["name"] == "User Service")
        api_gw   = next(s for s in self.services if s["name"] == "API Gateway")
        if self.scenario["state"] == "MITIGATING":
            user_svc["latency"] = max(100, user_svc["latency"] - 250)
            api_gw["latency"]   = max(95,  api_gw["latency"]   - 200)
            self._append_log(user_svc, "INFO", "[RECOVERY] Redis cluster replica promoted — cache warming in progress")
            if user_svc["latency"] <= 200:
                user_svc["status"] = "HEALTHY"
                self._recovery_done("API Gateway", "inc-demo-cache")
            return
        lat_add = [0, 100, 300, 700, 1400, 2600]
        idx = min(t, len(lat_add) - 1)
        user_svc.update({"status": "DEGRADED" if t < 4 else "CRITICAL", "latency": 105 + lat_add[idx], "lastUpdated": now_iso()})
        api_gw.update({"status": "DEGRADED" if t < 4 else "CRITICAL",  "latency": 95  + lat_add[idx], "lastUpdated": now_iso()})
        self.metrics.append(self._metric_for(user_svc))
        if t in {1, 2}:
            self._append_log(user_svc, "WARN", f"Redis cache hit rate dropped to {max(5, 85 - t*20)}% — read-through load increasing")
        if t >= 3:
            self._append_log(user_svc, "ERROR", "Redis primary unreachable — all cache reads falling through to database")
        if t >= 4:
            self._ensure_demo_incident("inc-demo-cache", "Redis/Cache Failure", "HIGH", "User Service",
                "Redis primary node failure causing full cache miss storm — DB under write pressure.")

    def _scenario_network_timeout(self) -> None:
        self.scenario["ticks"] += 1
        t = self.scenario["ticks"]
        api_gw = next(s for s in self.services if s["name"] == "API Gateway")
        if self.scenario["state"] == "MITIGATING":
            api_gw["latency"]   = max(95, api_gw["latency"] - 300)
            api_gw["errorRate"] = round(max(0.2, api_gw["errorRate"] - 3.0), 2)
            self._append_log(api_gw, "INFO", "[RECOVERY] Circuit breaker reset — upstream connectivity restored")
            if api_gw["latency"] <= 200:
                self._recovery_done("API Gateway", "inc-demo-net")
            return
        lat_curve = [100, 250, 700, 1600, 3200, 5800]
        err_curve = [0.3,  1.5,  5.0, 12.0,  22.0, 35.0]
        idx = min(t, len(lat_curve) - 1)
        api_gw.update({"status": "DEGRADED" if t < 4 else "CRITICAL", "latency": lat_curve[idx], "errorRate": err_curve[idx], "lastUpdated": now_iso()})
        self.metrics.append(self._metric_for(api_gw))
        if t in {1, 2}:
            self._append_log(api_gw, "WARN", f"Network timeout cascade: {t * 12}% upstream hops returning TCP RST")
        if t >= 3:
            self._append_log(api_gw, "ERROR", f"[trace-{t:05d}] Gateway timeout — all upstream service calls exceeding {lat_curve[idx]}ms")
        if t >= 4:
            self._ensure_demo_incident("inc-demo-net", "Network Timeout Cascade", "HIGH", "API Gateway",
                "API Gateway upstream connections timing out — possible network partition between AZ nodes.")

    def _ensure_demo_incident(self, iid: str, title: str, severity: str, service_name: str, summary: str) -> None:
        if any(i["id"] == iid for i in self.incidents):
            return
        svc = next((s for s in self.services if s["name"] == service_name), self.services[0])
        incident = {
            "id": iid,
            "title": title,
            "severity": severity,
            "serviceId": svc["id"],
            "service": service_name,
            "status": "INVESTIGATING",
            "detectedAt": now_iso(),
            "aiConfidence": None,
            "summary": summary,
            "timeline": [
                f"{now_iso()} Anomaly detected in {service_name} telemetry",
                f"{now_iso()} Threshold breach confirmed",
                f"{now_iso()} Incident automatically created",
            ],
        }
        self.incidents.insert(0, incident)
        self.activity.insert(0, {
            "timestamp": now_iso(),
            "event": f"CRITICAL incident detected: {title}",
        })

    def list_by_service(self, service_id: str, rows: list[dict]) -> list[dict]:
        return [deepcopy(r) for r in rows if r.get("serviceId") == service_id or service_id == "all"]

    def get_incident(self, incident_id: str) -> dict | None:
        incident = next((i for i in self.incidents if i["id"] == incident_id), None)
        if not incident:
            return None
        data = deepcopy(incident)
        data["logs"] = [l for l in self.logs if l["serviceId"] == incident["serviceId"]][-8:]
        data["metrics"] = self.list_by_service(incident["serviceId"], self.metrics)[-10:]
        data["analysis"] = next((a for a in reversed(self.analyses) if a["incident"] == incident_id), None)
        data["remediations"] = [r for r in self.remediations if r["incidentId"] == incident_id]
        return data

    def simulate_incident(self) -> dict:
        self.start_scenario("database_pool")
        for _ in range(6):
            self.tick()
        analysis = self.analyze_incident("inc-demo-db-pool")
        return {"incident": self.get_incident("inc-demo-db-pool"), "analysis": analysis}

    def analyze_incident(self, incident_id: str) -> dict:
        incident = next((i for i in self.incidents if i["id"] == incident_id), None)
        if not incident:
            raise KeyError(incident_id)
        logs = [l for l in self.logs if l["serviceId"] == incident["serviceId"]][-12:]
        metrics = [m for m in self.metrics if m["serviceId"] in {incident["serviceId"], "svc-7"}][-14:]
        analysis = self.ai_provider.analyze(incident, logs, metrics)
        incident["aiConfidence"] = analysis["confidence"]
        incident["timeline"].append(f"{now_iso()} Local AI analysis started")
        incident["timeline"].append(f"{now_iso()} Root cause identified")
        incident["timeline"].append(f"{now_iso()} Remediation recommended")
        self.analyses.append(analysis)
        for action in analysis["recommendedActions"]:
            if not any(r["id"] == action["id"] and r["incidentId"] == incident_id for r in self.remediations):
                self.remediations.append({**action, "incidentId": incident_id, "incident": incident["title"]})
        self.activity.insert(0, {"timestamp": now_iso(), "event": f"AI analysis completed for {incident['title']}"})
        return deepcopy(analysis)

    def execute_remediation(self, remediation_id: str) -> dict:
        remediation = next((r for r in self.remediations if r["id"] == remediation_id), None)
        if not remediation:
            raise KeyError(remediation_id)
        remediation["status"] = "Executing"
        remediation["status"] = "Monitoring"
        incident = next((i for i in self.incidents if i["id"] == remediation["incidentId"]), None)
        if incident:
            incident["timeline"].append(f"{now_iso()} Remediation executed")
        self.scenario["state"] = "MITIGATING"
        self.scenario["phase"] = "PHASE 6 - REMEDIATION"
        self.scenario["ticks"] = 0
        self.activity.insert(0, {"timestamp": now_iso(), "event": f"Simulated remediation executed: {remediation['action']}"})
        return deepcopy(remediation)

    def benchmark(self, runs: int = 12) -> dict:
        incident = self.incidents[0]
        latencies = []
        for _ in range(max(3, min(runs, 50))):
            started = time.perf_counter()
            self.ai_provider.analyze(incident, [], [])
            latencies.append((time.perf_counter() - started) * 1000)
        total = sum(latencies) / 1000
        self.performance = {"runs": len(latencies), "averageLatencyMs": round(statistics.mean(latencies), 3), "minimumLatencyMs": round(min(latencies), 3), "maximumLatencyMs": round(max(latencies), 3), "throughputPerSecond": round(len(latencies) / total, 2) if total else "Not measured", "modelSize": "Not measured", "memoryUsage": "Not measured", "accuracy": "Not measured", "updatedAt": now_iso()}
        return deepcopy(self.performance)


edge_store = EdgeDemoStore()
