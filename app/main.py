
# Import the LLM initialization function
from app.config import get_llm

# Import the system prompt
from app.prompts import SYSTEM_PROMPT


# Main application function
def run_chat():

    # Initialize the LLM
    llm = get_llm()

    # Create conversation history
    chat_history = []

    # Display welcome message
    print("\n======================================")
    print("     AI INTERVIEW PREPARATION MENTOR")
    print("======================================")
    print("Ask me your interview questions.")
    print("Type 'exit' to close the application.")
    print("======================================")


    # Keep the conversation running
    while True:

        try:

            # Get user input
            question = input("\nYou: ").strip()


            # Exit condition
            if question.lower() in ["exit", "quit", "bye"]:
                print("\nAI Mentor: Goodbye! Happy learning!")
                break


            # Validate empty input
            if not question:
                print("Please enter a question.")
                continue


            # Prepare conversation messages
            messages = [
                ("system", SYSTEM_PROMPT)
            ] + chat_history + [
                ("human", question)
            ]


            # Generate AI response
            response = llm.invoke(messages)

            answer = response.content


            # Display response
            print("\nAI Mentor:")
            print(answer)


            # Update conversation history
            chat_history.append(("human", question))

            chat_history.append(("ai", answer))


        except KeyboardInterrupt:

            print("\n\nApplication stopped by user.")
            break


        except Exception as error:

            print(f"\nAn error occurred: {error}")


# Application entry point
if __name__ == "__main__":

    run_chat()
