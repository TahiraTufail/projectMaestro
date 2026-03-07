import os,json,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from openai import OpenAI
from dotenv import load_dotenv
from tools.os_manager_tool import invoke_os_manager, os_manager_tool
from tools.coder_manager_tool import invoke_coder_agent, coder_agent_tool
"""gather data from multiple  agents and collaborate them"""

load_dotenv()

class MasterAgent:
    def __init__(self,max_reflect_steps=3):
        self.__llm = OpenAI(api_key=os.getenv("OPENAI_API"))
        self.__max_reflect_steps = max_reflect_steps
        self.__tool_agents_executed = False
        with open('./agents/supervisor/system_message.txt', 'r') as f:
            self.system_message = f.read()
        with open('./agents/supervisor/critique_message.txt', 'r') as f:
            self.critique_message = f.read()

    def invoke(self, user_instruction: str):
        self.__tool_agents_executed = False
        actor_input = user_instruction
        actor_messages = [{'role': 'system', 'content': self.system_message}]
        critique_messages = [{'role': 'system', 'content': self.critique_message}]
        for i in range(self.__max_reflect_steps):
            actor_messages.append({'role':'user','content': actor_input})
            actor_response = self.__response_generator(actor_messages, role = 'actor')
            critique_messages.append({'role':'user','content':actor_response})
            critique_response = self.__response_generator(critique_messages, role= 'critique')
            if critique_response.__contains__("$OK$"):
                break
            actor_input = critique_response
        return actor_response
            
    def __response_generator(self,messages: list[dict],role):
        if role == "actor":
            response_format = {'type':'json_object'}
        else:
            response_format = {'type': 'text'}
        if not self.__tool_agents_executed:
            response = self.__llm.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools = [os_manager_tool, coder_agent_tool],
                response_format=response_format
            )
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_response = self.__handle_tool_call(message)
                messages.append(message)
                messages += tool_response
                response = self.__llm.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    response_format=response_format
                )
                self.__tool_agents_executed = True
        else:
            response = self.__llm.chat.completions.create(
                model='gpt-4o-mini',
                messages= messages,
                response_format= response_format
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


    