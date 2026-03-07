import os,sys
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
        response = self.__llm.models.generate_content(
            model= "gemini-2.5-flash-preview-04-17",
            contents= [self.reason_prompt ,user_instruction]
        )
        return response.text    