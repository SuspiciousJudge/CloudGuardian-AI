from google.adk.tools import ToolContext


def exit_loop(tool_context: ToolContext) -> dict:
    """
    Exits the remediation loop when fixes are confirmed complete.
    """
    tool_context.actions.escalate = True
    return {
        "status": "remediation_complete",
        "message": "Loop exited successfully"
    }
