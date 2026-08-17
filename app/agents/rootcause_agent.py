from google.adk.agents import Agent

rootcause_agent = Agent(
    name="rootcause_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a root cause analysis expert for cloud incidents.

    Analyze all inputs:

    Log Analysis:
    {log_analysis}

    Infrastructure Analysis:
    {infra_analysis}

    Security Analysis:
    {security_analysis}

    Your job:
    1. Correlate findings from logs, infrastructure, and security
    2. Identify the PRIMARY root cause
    3. Identify any CONTRIBUTING factors
    4. Assign severity level: CRITICAL / HIGH / MEDIUM / LOW
    5. Estimate time to resolution

    Output a precise root cause analysis report.
    """,
    output_key="root_cause"
)
