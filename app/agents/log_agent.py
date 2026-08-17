from google.adk.agents import Agent
from app.tools.gcp_logs_tool import analyze_logs

log_agent = Agent(
    name="log_agent",
    model="gemini-2.5-flash",
    tools=[analyze_logs],
    instruction="""
    You are a production log analysis expert.

    Your job:
    1. Call analyze_logs tool with the service name from the user query
    2. Carefully analyze all log entries
    3. Identify error patterns, failure types, and severity
    4. Summarize findings clearly

    Output a structured log analysis summary.
    """,
    output_key="log_analysis"
)
