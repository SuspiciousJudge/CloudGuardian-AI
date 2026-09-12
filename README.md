# CloudGuardian Edge
> Detect. Diagnose. Respond — Locally.

CloudGuardian Edge is a privacy-first, on-device AI incident response platform built for the edge computing era. It analyzes application logs and infrastructure telemetry natively on the local device, detects incidents, conducts root-cause analysis (RCA), and recommends remediation, all without sending proprietary data to the cloud.

## The Problem
Today's observability engines are highly dependent on cloud infrastructure. Streaming terabytes of telemetry data off-site to a centralized Cloud AI incurs excessive egress costs, introduces latency that delays critical remediation, creates massive data privacy concerns for sensitive logs, and removes the ability for autonomous edge sites to self-heal when disconnected from the internet.

## The Solution
CloudGuardian Edge brings the AI to the telemetry. By analyzing metrics and logs locally using an on-device architecture, we can leverage edge compute to diagnose and remediate issues in milliseconds.

## Features
* **Wait-Free Live Telemetry:** Streaming data visualization via Server-Sent Events (SSE).
* **Deterministic Incident Simulation Engine:** Simulates 8 complex degradation failure modes in real-time.
* **On-Device RCA:** An abstraction boundary designed to support hardware-accelerated local AI inference.
* **Automated Remediation execution:** Self-healing simulation that smoothly transitions a recovered state.

## Architecture & Simulation Engine
The hackathon demo includes an advanced deterministic backend built with `FastAPI` to maintain the illusion of a full multi-tenant microservices deployment.
Using an event-loop background tick process, it synthesizes real-world load variations and fault profiles, including:
1. Database Connection Pool Exhaustion
2. Payment API Latency Spike
3. Authentication Failure Spike
4. Memory Leak
5. Container Crash Loop
6. CPU Saturation
7. Redis/Cache Failure
8. Network Timeout Cascade

## Qualcomm Snapdragon Optimization Target
This stack was built with an explicit path toward production deployment on Snapdragon-powered edge units. Refer to `docs/SNAPDRAGON.md` to see the proposed architecture integrating the **Qualcomm AI Hub**.

## Local Setup & Demo Instructions

### 1. Requirements
- Python 3.10+

### 2. Quickstart
```bash
# Clone the directory & setup virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastApi demo server on port 8000
python -m uvicorn app.main:app --port 8000 --reload
```

### 3. Demo Controls
1. Visit `http://localhost:8000/ui` in your browser.
2. The UI will instantly begin streaming live baseline metric data across 8 microservices.
3. Use the **Demo Controls** bar at the top to select a scenario and click **Start Incident**.
4. Watch the charts, logs, and system health status respond to the simulated stress natively.
5. Click **View Incident** when the anomaly is detected and use the **Local AI Analysis** to pinpoint the root cause natively.
6. Trigger the **Remediation** step to witness the backend resolve the incident loop and restore system metrics smoothly back to baseline.

## Limitations & Future Work
- The AI Engine currently utilizes a fast deterministic heuristic strategy rather than an actual weight-loaded Local LLM mapping for the sake of portable, dependency-free localhost hackathon evaluation.
- Future work will bridge our generic `AIProvider` wrapper to directly invoke Qualcomm AI Hub optimized NLP classification pipelines.
