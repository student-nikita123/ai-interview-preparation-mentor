
# Import ChatOllama from LangChain
from langchain_ollama import ChatOllama


# Create an object of the LLM
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.2
)


# Define the system prompt
system_prompt = """
You are an experienced Technical Interview Preparation Mentor.

Your responsibility is to help beginners prepare for technical interviews.

Follow these instructions:

1. Explain every concept using simple English.
2. Assume the user is a beginner.
3. Start with a clear and simple definition.
4. Explain why the concept is important.
5. Provide practical examples wherever possible.
6. For programming questions, provide code examples
   and explain the important lines.
7. Provide an interview-ready answer.
8. Be supportive, patient and encouraging.
9. If the user gives an incorrect answer,
   explain the mistake politely.
10. Do not make up technical facts.
    If you are unsure, clearly mention it.
11. Keep explanations structured and easy to understand.

Use previous conversation messages to understand
the user's follow-up questions.
"""


# Create an empty list for conversation history
chat_history = []


# Display the application welcome message
print("\n==========================================")
print("       AI INTERVIEW PREPARATION MENTOR")
print("==========================================")
print("Welcome! Ask me your interview questions.")
print("Type 'exit' to close the application.")
print("==========================================")


# Keep the application running
while True:

    try:

        # Take input from the user
        question = input("\nYou: ").strip()


        # Check whether the user wants to exit
        if question.lower() in ["exit", "quit", "bye"]:
            print("\nAI Mentor: Goodbye! Happy learning!")
            break


        # Check whether the input is empty
        if not question:
            print("Please enter a question.")
            continue


        # Prepare the complete conversation messages
        messages = [
            ("system", system_prompt)
        ] + chat_history + [
            ("human", question)
        ]


        # Send the messages to the LLM
        response = llm.invoke(messages)


        # Extract the generated answer
        answer = response.content


        # Display the AI response
        print("\nAI Mentor:")
        print(answer)


        # Store the user question in history
        chat_history.append(("human", question))


        # Store the AI response in history
        chat_history.append(("ai", answer))


    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")
        break


    except Exception as error:
        print(f"\nAn error occurred: {error}")
