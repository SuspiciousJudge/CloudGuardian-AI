from google.adk.agents import LoopAgent, Agent

recommendation_loop_agent = Agent(
    name="recommendation_loop_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a remediation specialist.
    Suggest improved remediation steps based on previous attempts.
    Be specific and actionable.
    """,
    output_key="loop_recommendations"
)

report_loop_agent = Agent(
    name="report_loop_agent",
    model="gemini-2.5-flash",
    instruction="""
    Generate a remediation progress report.

    Current Recommendations:
    {loop_recommendations}

    Summarize what has been attempted and current status.
    """
)

remediation_loop = LoopAgent(
    name="remediation_loop",
    sub_agents=[
        recommendation_loop_agent,
        report_loop_agent
    ],
    max_iterations=3
)
