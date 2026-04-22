import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

llm = ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4.1-mini",
)
