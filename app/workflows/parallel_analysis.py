from google.adk.agents import ParallelAgent
from app.agents.log_agent import log_agent
from app.agents.infra_agent import infra_agent
from app.agents.security_agent import security_agent

parallel_analysis = ParallelAgent(
    name="parallel_analysis",
    sub_agents=[
        log_agent,
        infra_agent,
        security_agent
    ]
)
