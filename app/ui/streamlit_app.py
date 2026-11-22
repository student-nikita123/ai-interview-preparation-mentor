"""Streamlit interface for the AI Interview Preparation Mentor."""

import logging

import streamlit as st

from app.config import get_llm
from app.services.chat import MAX_QUESTION_LENGTH, generate_answer

LOGGER = logging.getLogger(__name__)
SUGGESTED_QUESTIONS = (
    "Explain object-oriented programming with a simple example.",
    "How should I answer, “Tell me about yourself”?",
    "What is the difference between a list and a tuple in Python?",
)

st.set_page_config(
    page_title="Interview Prep Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_llm():
    """Create one reusable local language-model client."""
    return get_llm()


def render_sidebar() -> None:
    """Show app information and conversation controls."""
    with st.sidebar:
        st.markdown("## 🎓 Interview Mentor")
        st.caption("Your supportive partner for technical interview practice.")
        st.divider()
        st.markdown("**Powered by**")
        st.markdown("Ollama · Llama 3.2")
        st.caption("Responses are generated locally by your configured Ollama model.")

        if st.button("＋  Start a new chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pending_question = None
            st.rerun()

        st.divider()
        st.caption("Tip: Ask a follow-up to explore a topic in more depth.")


def render_messages() -> None:
    """Display the current conversation using Streamlit's chat components."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def submit_question(question: str) -> None:
    """Generate and display a response, reporting model errors to the user."""
    history = [
        ("human" if message["role"] == "user" else "ai", message["content"])
        for message in st.session_state.messages
    ]

    try:
        with st.spinner("Thinking through your question..."):
            answer = generate_answer(load_llm(), question, history)
    except ValueError as error:
        st.warning(str(error))
        return
    except Exception as error:
        LOGGER.exception("Unable to generate a mentor response.")
        st.error(
            "I couldn't get a response from the local model. "
            "Check that Ollama is running and that the configured model "
            "is available, then try again."
        )
        st.caption(f"Details: {error}")
        return

    with st.chat_message("user"):
        st.markdown(question.strip())
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.extend(
        [
            {"role": "user", "content": question.strip()},
            {"role": "assistant", "content": answer},
        ]
    )


def main() -> None:
    """Render the mentor interface and handle submitted questions."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    render_sidebar()

    st.markdown("# Your AI Interview Prep Mentor")
    st.markdown(
        "Build confidence for your next interview with clear explanations, "
        "practical examples, and thoughtful follow-ups."
    )

    if not st.session_state.messages:
        st.info(
            "Start with a question about a technical concept, coding problem, "
            "or interview practice."
        )
        st.markdown("#### Not sure where to begin?")
        columns = st.columns(len(SUGGESTED_QUESTIONS))
        for index, (column, suggested_question) in enumerate(
            zip(columns, SUGGESTED_QUESTIONS)
        ):
            with column:
                if st.button(
                    suggested_question,
                    key=f"suggestion_{index}",
                    use_container_width=True,
                ):
                    st.session_state.pending_question = suggested_question

    render_messages()

    question = st.chat_input(
        "Ask an interview preparation question...",
        max_chars=MAX_QUESTION_LENGTH,
    )
    pending_question = st.session_state.pending_question
    st.session_state.pending_question = None

    if pending_question:
        submit_question(pending_question)
    elif question:
        submit_question(question)


if __name__ == "__main__":
    main()
