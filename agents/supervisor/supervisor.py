import os,json,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from openai import OpenAI
from dotenv import load_dotenv
from tools.os_manager_tool import invoke_os_manager, os_manager_tool
from tools.coder_manager_tool import invoke_coder_agent, coder_agent_tool
"""gather data from multiple  agents and collaborate them"""

load_dotenv()

class MasterAgent:
    def __init__(self):
        self.__llm = OpenAI(api_key=os.getenv("OPENAI_API"))
        with open('./agents/supervisor/system_message.txt', 'r') as f:
            self.system_message = f.read()
        

    def invoke(self, user_instruction: str):
        messages= [
            {'role':'system', 'content': self.system_message},
            {'role':'user', 'content': user_instruction}
        ]
        response = self.__llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools = [os_manager_tool, coder_agent_tool],
            temperature= 0
        )
        if response.choices[0].finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_response = self.__handle_tool_call(message)
            messages.append(message)
            messages += tool_response
            response = self.__llm.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature= 0
            )
        return response.choices[0].message.content
    
    def __handle_tool_call(self, message):
        tool_calls = message.tool_calls
        tool_responses = []
        for tool_call in tool_calls:
            if tool_call.function.name == 'invoke_os_manager':
                arguments = json.loads(tool_call.function.arguments)
                task = arguments.get("task")
                response = invoke_os_manager(task)
                tool_response = {
                    'role':'tool',
                    'content':json.dumps({"os_manager_response": response}),
                    'tool_call_id' : tool_call.id
                }
                tool_responses.append(tool_response)
            else:
                arguments = json.loads(tool_call.function.arguments)
                task = arguments.get("task")
                response = invoke_coder_agent(task)
                tool_response = {
                    'role':'tool',
                    'content':json.dumps({"coder_agent_response": response}),
                    'tool_call_id' : tool_call.id
                }   
                tool_responses.append(tool_response)
        return tool_responses    