import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.coder.coder_g import CodeAgent

coder_agent = CodeAgent()
#tool...
def invoke_coder_agent(task: str):
    response = coder_agent.invoke(task)
    return response

coder_agent_tool = {
    "type": "function",
    "function": {
        "name": "invoke_coder_agent",
        "description": "This tool is used to delegate code-related tasks to the coder agent (e.g., generate code etc).",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "A detailed coding task that the coder agent should execute."
                }
            },
            "required": ["task"],
            "additionalProperties": False
        },
        "strict": True
    }
}


    