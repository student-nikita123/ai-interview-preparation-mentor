
# Import ChatOllama from LangChain
from langchain_ollama import ChatOllama


# Define the model configuration
MODEL_NAME = "llama3.2:latest"

TEMPERATURE = 0.2


# Function to initialize the LLM
def get_llm():

    llm = ChatOllama(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )

    return llm
