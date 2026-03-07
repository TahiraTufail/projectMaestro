import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from openai import OpenAI
from dotenv import load_dotenv

"""gather data from multiple  agents and collaborate them"""

load_dotenv()

class CodeManagerAgent:
    def __init__(self, max_reflect_steps=3):
        self.__llm = OpenAI(api_key=os.getenv("OPENAI_API"))
        self.__max_reflect_steps = max_reflect_steps
        with open('./agents/coder/system_prompt.txt', 'r') as f:
            self.system_prompt = f.read()
        with open('./agents/coder/critique_prompt.txt', 'r') as f:
            self.critique_prompt = f.read()

    def invoke(self, user_instruction: str):
        actor_input = user_instruction
        actor_messages = [{'role': 'system', 'content': self.system_prompt}]
        critique_messages = [{'role': 'system', 'content': self.critique_prompt}]
        for i in range(self.__max_reflect_steps):
            actor_messages.append({'role':'user','content': actor_input})
            actor_response = self.__response_generator(actor_messages)
            print(i+1)
            critique_messages.append({'role':'user','content':actor_response})
            critique_response = self.__response_generator(critique_messages)
            if critique_response.__contains__("$OK$"):
                break
            actor_input = critique_response
        return actor_response
    
    def __response_generator(self,messages: list[dict]):
        return self.__llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        ).choices[0].message.content

    