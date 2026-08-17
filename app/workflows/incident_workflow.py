from google.adk.agents import SequentialAgent
from app.workflows.parallel_analysis import parallel_analysis
from app.agents.rootcause_agent import rootcause_agent
from app.agents.recommendation_agent import recommendation_agent
from app.agents.report_agent import report_agent

incident_workflow = SequentialAgent(
    name="incident_workflow",
    sub_agents=[
        parallel_analysis,
        rootcause_agent,
        recommendation_agent,
        report_agent
    ]
)
