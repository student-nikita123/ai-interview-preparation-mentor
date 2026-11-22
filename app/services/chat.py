"""Chat operations for the interview preparation mentor."""

from collections.abc import Sequence

from langchain_core.language_models.chat_models import BaseChatModel

from app.prompts import SYSTEM_PROMPT

MAX_QUESTION_LENGTH = 4000


def generate_answer(
    llm: BaseChatModel,
    question: str,
    chat_history: Sequence[tuple[str, str]] = (),
) -> str:
    """Validate a question and return the mentor's response."""
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")
    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError(
            f"Questions must be {MAX_QUESTION_LENGTH} characters or fewer."
        )

    messages = [("system", SYSTEM_PROMPT), *chat_history, ("human", question)]
    response = llm.invoke(messages)
    answer = response.content

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("The model returned an empty or unsupported response.")

    return answer.strip()
