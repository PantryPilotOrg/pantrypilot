import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


llm = ChatOpenAI(
    api_key=os.getenv("LLMOD_API_KEY"),
    base_url=os.getenv("LLMOD_BASE_URL"),
    model="NBUECSE-gpt-5-mini",
)