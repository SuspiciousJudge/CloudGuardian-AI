from google.adk.agents import Agent
from app.tools.monitoring_tool import check_infra
from app.tools.kubernetes_tool import check_kubernetes_status

infra_agent = Agent(
    name="infra_agent",
    model="gemini-2.5-flash",
    tools=[check_infra, check_kubernetes_status],
    instruction="""
    You are an infrastructure health analysis expert.

    Your job:
    1. Call check_infra tool with the service name
    2. Call check_kubernetes_status tool with the service name
    3. Analyze CPU, memory, network, and pod status
    4. Identify infrastructure-level problems

    Output a structured infrastructure analysis summary.
    """,
    output_key="infra_analysis"
)
