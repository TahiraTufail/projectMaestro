from openai import OpenAI
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from dotenv import load_dotenv

"""gather data from multiple  agents and collaborate them"""

load_dotenv()

class OSManagerAgent:
    def __init__(self):
        self.__llm = OpenAI(api_key=os.getenv("OPENAI_API"))
        with open('./agents/os_manager/system_message.txt', 'r') as f:
            self.system_message = f.read()
         

    def invoke(self, user_instruction: str):
        user_instruction = f'''Given the following user instruction, generate only the necessary OS commands (for Windows by default):
"{user_instruction}"

Focus exclusively on file system operations such as:
- Navigating to appropriate directories
- Creating directories and files
- Setting up proper paths and permissions
- Any other file system tasks needed
- Create the code.bat file, execute it and then delete it.

Do not include any code implementation details or explanations.
Respond only with the command sequence, with each command on its own line.
'''
        response = self.__llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {'role':'system', 'content': self.system_message},
                {'role':'user', 'content': user_instruction}
            ],
            temperature= 0
        ).choices[0].message.content
        return response
if __name__ == "__main__":
    agent = OSManagerAgent()
    response = agent.invoke("Set up a React project called task-manager with a basic component structure including Header, TaskList, and TaskForm components. Include a basic CSS file with styling for these components.")
    print(response)