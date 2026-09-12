# CloudGuardian Edge
> Detect. Diagnose. Respond — Locally.

---

## 2. The Problem
- Cloud observability platforms are dominant but fundamentally constrained by internet dependencies.
- Streaming logs per second off-device creates **massive egress costs**, **privacy risks**, and **high latency** for time-sensitive remediation actions.

---

## 3. Existing Cloud AI Limitations
- **Opex Costs:** Paying token fees for every single telemetry event.
- **Vulnerability:** If the network goes down, you lose visibility and automated remediation.
- **Privacy Barrier:** Financial, medical, and defense use cases physically cannot upload infrastructure footprints to public LLM endpoints.

---

## 4. CloudGuardian Edge Solution
- **Edge-First AI Response:** Move the intelligence to the application edge node.
- Ingest logs offline via local daemons, evaluate faults in-memory, and perform GenAI Root Cause Analysis directly out of local hardware.
- Result: **0ms egress latency. Absolute privacy. Infinite scalability without cloud limits.**

---

## 5. Live Architecture
- FastAPI streams Server-Sent Events natively to a unified dashboard.
- The simulation engine generates deterministic application states (HTTP Latency Spikes, Pod CrashLoops).
- Live metrics directly hydrate the React-style charting engine without requiring polling.

---

## 6. AI Architecture
- We abstracted the LLM with an `AIProvider`.
- Currently loaded: `Local Demo Engine`, demonstrating instantaneous heuristic telemetry evaluation.
- Drop-in ready: ONNX runtime loading language models optimized for NPU silicon.

---

## 7. Live Incident Demo
- [Switch to Live Demo: Starting the UI, showcasing baseline metrics]
- Let's initiate the "Database Connection Pool Exhaustion" simulated fault.
- Notice the cascade across memory, connection allocation limits, and UI timeouts streaming live.

---

## 8. Root Cause Analysis
- [In Demo: Clicking Local AI Analysis]
- Instead of searching Splunk, our Edge Agent instantly correlates high DB utilization coupled with HTTP timeouts, resulting in a localized diagnosis within ~350 milliseconds.

---

## 9. Remediation
- [In Demo: Executing Remediation]
- Acknowledging the issue immediately executes local actions (e.g. killing zombie workers, scaling pools). 
- We see latency recovery occur natively within 3 state ticks. 

---

## 10. Performance
- On our localhost setup, typical AI insight loop requires <500ms from telemetry evaluation to decision matrix output.
- Because data stays in-memory, we save standard 2-second cloud round-trip times per transaction.

---

## 11. Snapdragon Optimization
- **Why Snapdragon?** NPUs are built for exactly this—sustained inference pipelines at exceptionally low power footprints.
- We constructed the CloudGuardian boundaries explicitly mapping to the Qualcomm AI Hub roadmap. 
- Edge-routers, IoT factories, and PC workstations can leverage their onboard silicon for self-repair functionality natively using CloudGuardian.

---

## 12. Impact + Roadmap
- We've proven the capability for robust, privacy-first edge intelligence.
- **Next Steps:** Hardware acceleration benchmarking on the latest Snapdragon platforms and expanding our fault signature classification dataset.
