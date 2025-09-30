from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class LangChain:
    def __init__(self):
        load_dotenv()
        self.openai = ChatOpenAI(model="gpt-4o", temperature=0.1)
        self.anthropic = ChatAnthropic(model_name="claude-sonnet-4-20250514", temperature=0.1)
        