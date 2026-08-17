from google.adk.agents import Agent

recommendation_agent = Agent(
    name="recommendation_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a senior DevOps engineer and cloud architect.

    Root Cause:
    {root_cause}

    Your job:
    1. Provide immediate remediation steps (do RIGHT NOW)
    2. Provide short-term fixes (next 24 hours)
    3. Provide long-term prevention steps
    4. Provide exact commands where applicable
    5. Prioritize steps by impact

    Output a detailed, actionable remediation plan.
    """,
    output_key="recommendations"
)
