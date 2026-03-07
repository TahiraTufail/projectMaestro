import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.os_manager.os_manager import OSManagerAgent

os_agent = OSManagerAgent()
def invoke_os_manager(task:str):
    response = os_agent.invoke(task)
    return response

os_manager_tool = {
    "type": "function",
    "function": {
        "name": "invoke_os_manager",
        "description": "This function is used to call the os manager agent to provide the os related commands",
        "parameters": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "A detailed task that the os agent has to execute"
                }
            },
            "required": [
                "task"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}