# CloudGuardian Edge & Qualcomm Snapdragon AI Hub

## Why Target On-Device AI for Incident Response?

Enterprise incident response conventionally relies on streaming raw logs and metrics from production environments into cloud aggregation services (Datadog, Splunk, etc.). From there, cloud-based models perform Root Cause Analysis. This approach comes with severe drawbacks:

1. **Egress Costs:** Shipping terabytes of telemetry simply to detect localized faults is prohibitively expensive.
2. **Latency:** Cloud round-trips delay the time-to-remediation for critical automation loops.
3. **Connectivity:** Edge computing environments (IoT, disconnected industrial sites) cannot guarantee access to cloud APIs.
4. **Data Privacy:** Exporting sensitive production logs to external GenAI endpoints introduces massive infosec risk.

## The CloudGuardian Edge Architecture
By positioning an AI agent directly on the edge node, CloudGuardian reads logs and memory arrays directly from the localhost interface without touching the public internet.

### Integration with Snapdragon
Our `AIProvider` boundary is designed as a direct integration point for the **Qualcomm AI Hub**. 
While the current localhost demo utilizes a deterministic fallback layer to ensure it runs out-of-the-box for demo environments, the target production architecture executes PyTorch/ONNX models specifically compiled for the Snapdragon NPU.

```text
Local Telemetry (StatsD/Syslog) 
  --> Preprocessing (Local Python context) 
    --> Snapdragon NPU (Qualcomm-optimized on-device LLM inference) 
      --> Postprocessing Agent 
        --> Automated Remediation (Local Docker API / Kubernetes control plane)
```

By leveraging the NPU of Snapdragon-powered compute environments (such as Snapdragon X Elite PCs or industrial Windows IoT edge gateways), CloudGuardian achieves low-power, high-speed telemetry reasoning.

### Performance & Benchmarking
In the "Model Performance" section of the dashboard, you can trigger a benchmark test. For this submission, our objective was validating the workflow application architecture. As we adopt physical Snapdragon deployment targets natively executing LLaMA or Mistral equivalents via the Qualcomm AI Hub, these benchmarks will accurately reflect the sub-millisecond inferences generated directly on device.
