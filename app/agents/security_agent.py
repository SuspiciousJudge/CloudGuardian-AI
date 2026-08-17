from google.adk.agents import Agent
from app.tools.security_scan_tool import scan_security

security_agent = Agent(
    name="security_agent",
    model="gemini-2.5-flash",
    tools=[scan_security],
    instruction="""
    You are a cloud security analysis expert.

    Your job:
    1. Call scan_security tool with the service name
    2. Analyze threat indicators, failed logins, suspicious IPs
    3. Determine if security is a contributing factor to the incident

    Output a structured security analysis summary.
    """,
    output_key="security_analysis"
)
