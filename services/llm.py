import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

BASE_URL = "https://backend.sovereigneg.com/v1"
API_KEY = os.getenv("SOVEREIGNEG_API_KEY")
MODEL = "gpt-4.1-nano"

class InstrumentedLLM:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
            model=MODEL,
            temperature=0,
        ) 
        # TODO: this class will be extended
    
    def get_llm(self):
        return self.llm 

    def get_llm_with_structured_output(self, output_format):
        return self.llm.with_structured_output(output_format)

    @staticmethod
    async def llm_text(llm: ChatOpenAI, system_prompt: str, user_prompt: str) -> str:
        response = await llm.ainvoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        ) 
        return str(response.content)

instrumented_llm = InstrumentedLLM()
