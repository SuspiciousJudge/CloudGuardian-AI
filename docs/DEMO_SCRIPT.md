# CloudGuardian Edge Demo Script

## Duration: ~3 minutes

### 0:00 - Introduction & Baseline
(Open the CloudGuardian Edge dashboard. Show the "System Overview")
"This is CloudGuardian Edge, an edge-first AI incident response platform. As you can see, normally the system is healthy and telemetry is continuously generated. We are operating completely offline right now."

### 0:30 - Live Telemetry
(Click on the Services and Live Logs tabs to show metrics streaming in real-time)
"We have live metrics and logs updating natively in real-time, tracking memory, latency, and CPU metrics without sending data off-device."

### 0:45 - The Incident
(Go back to Overview, under Demo Controls select "Database Connection Pool Exhaustion")
"Now, let's inject a real-world failure."
(Click `START INCIDENT`)

### 1:00 - Degradation
"Let's watch as the system reacts. We can see CPU spiking, connection pools draining, and eventually, request latency spiking enormously as the cascading failure hits the Payment Service."

### 1:15 - Critical Incident
"The application has automatically detected the metrics anomaly and generated a Critical Incident."

### 1:30 - Open Incident
(Click View/Inspect Incident)
"Let's inspect the incident timeline and metrics."

### 1:40 - Local AI
"Instead of sending proprietary telemetry to a cloud LLM and incurring latency, we run our RCA agent locally."
(Click `ANALYZE WITH LOCAL AI`)

### 1:55 - RCA Results
"Our deterministic edge logic (which acts as a stand-in for our Snapdragon-optimized local model) has instantly correlated the timeout logs and latency spikes to accurately identify Database Connection Pool Exhaustion. It provides a 94.2% confidence score based on concrete evidence."

### 2:10 - Remediation 
"The agent has also proposed an immediate remediation step to safely relieve connection pressure."

### 2:20 - Execution
(Click `EXECUTE REMEDIATION`)
"We apply the remediation autonomously."

### 2:35 - Recovery
"Notice how the latency drops, errors subside, and the system restores itself smoothly back to the healthy state, automatically marking the incident as mitigated."

### 2:45 - Model Benchmark
(Navigate to Model Performance. Click `RUN BENCHMARK SERIES`)
"Because we operate on-device, our inference loop avoids network latency completely. We processed this incident rapidly, highlighting the value of edge-AI."

### 3:00 - Snapdragon Optimization Wrap-up
"We've designed CloudGuardian Edge so that its AI Provider abstraction can easily swap into the Qualcomm Snapdragon AI Hub, scaling this offline intelligence natively to the edge."
