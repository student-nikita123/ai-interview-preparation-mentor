# Import ChatOllama from LangChain
from langchain_ollama import ChatOllama


# Create an object of the ChatOllama class
llm = ChatOllama(model="llama3.2:latest")


# Take input from the user
question = input("Ask your question: ")


# Send the question to the LLM
response = llm.invoke(question)


# Display the AI response
print("\nAI Mentor:")
print(response.content)