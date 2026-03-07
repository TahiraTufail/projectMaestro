import os,sys,json
from google import genai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from dotenv import load_dotenv

load_dotenv()
class CodeAgent:
    
    def __init__(self):
        self.__llm = genai.Client(api_key= os.getenv('GEMINI_API'))
        with open('./agents/coder/reason_prompt.txt', 'r') as f:
            self.reason_prompt = f.read()
    
    def invoke(self,user_instruction : str ):
        user_instruction = f'''Given the following user instruction, generate only the code implementation:
"{user_instruction}"

Focus exclusively on the programming aspects:
- Use appropriate language, frameworks, and libraries
- Include all necessary imports and dependencies
- Implement the complete functionality as specified
- Follow best practices for the chosen language
- Include proper error handling where appropriate

Do not include any OS commands, file operations, or explanations.
Respond only with the complete code implementation.
'''
        response = self.__llm.models.generate_content(
            model= "gemini-2.5-flash-preview-04-17",
            contents= [self.reason_prompt ,user_instruction]
        )
        return response.text    
if __name__ == "__main__":
    agent = CodeAgent()
    response = agent.invoke("Set up a React project called task-manager with a basic component structure including Header, TaskList, and TaskForm components. Include a basic CSS file with styling for these components.")
    print(response)