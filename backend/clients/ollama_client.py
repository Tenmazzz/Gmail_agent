from langchain_ollama import ChatOllama
import os

llm = ChatOllama(
    model=os.environ.get("OLLAMA_MODEL"),
    base_url=os.environ.get("OLLAMA_BASE_URL"),
    temperature=0.1
)