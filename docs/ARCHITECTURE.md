# Architecture

```text
Browser Dashboard
      |
      v
FastAPI Backend
      |
      +--> Demo Store: services, metrics, logs, incidents
      +--> Incident Engine: simulation, lifecycle, timelines
      +--> AI Layer: AIProvider -> LocalAIProvider
      +--> Remediation: safe simulated execution
      +--> Benchmarking: repeated local inference timings
```

## Frontend

Single static enterprise dashboard served from `app/ui/index.html`.

## Backend

FastAPI in `app/main.py` exposes `/api/dashboard`, services, incidents, logs, metrics, remediation, health, and model performance endpoints.

## Database

Current demo persistence is deterministic in-memory data in `app/edge_demo.py`.

## AI Layer

`AIProvider` keeps model integration separate from dashboard and API contracts.

## Local Inference

`LocalAIProvider` performs deterministic local demo analysis over telemetry. It is not a production LLM.

## Incident Engine

Simulation updates service health, metrics, logs, incident state, and activity.

## Remediation

Execution is simulated and non-destructive.

## Benchmarking

The benchmark endpoint runs local inference multiple times and measures latency.

## Snapdragon Integration Point

Add a Qualcomm AI Hub provider behind `AIProvider`.
