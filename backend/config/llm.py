import os

from langchain_ollama import ChatOllama

# Locally this defaults to http://localhost:11434 (your existing setup).
# In docker-compose, OLLAMA_BASE_URL is set to http://ollama:11434 so the
# app container can reach the ollama container by its service name.
llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0,
    format="json",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
)