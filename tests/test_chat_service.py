"""Tests for interview mentor chat validation and response handling."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from app.services.chat import MAX_QUESTION_LENGTH, generate_answer


class GenerateAnswerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.llm = Mock()
        self.llm.invoke.return_value = SimpleNamespace(content="  A clear answer.  ")

    def test_rejects_empty_question_without_calling_model(self) -> None:
        with self.assertRaisesRegex(ValueError, "enter a question"):
            generate_answer(self.llm, "   ")

        self.llm.invoke.assert_not_called()

    def test_rejects_question_over_maximum_length(self) -> None:
        with self.assertRaisesRegex(ValueError, "4000 characters"):
            generate_answer(self.llm, "q" * (MAX_QUESTION_LENGTH + 1))

        self.llm.invoke.assert_not_called()

    def test_returns_trimmed_answer_and_includes_history(self) -> None:
        history = [("human", "What is a class?"), ("ai", "A reusable blueprint.")]

        answer = generate_answer(self.llm, "  Give an example.  ", history)

        self.assertEqual(answer, "A clear answer.")
        messages = self.llm.invoke.call_args.args[0]
        self.assertEqual(messages[1:3], history)
        self.assertEqual(messages[-1], ("human", "Give an example."))

    def test_rejects_empty_model_response(self) -> None:
        self.llm.invoke.return_value = SimpleNamespace(content="  ")

        with self.assertRaisesRegex(RuntimeError, "empty or unsupported"):
            generate_answer(self.llm, "Explain recursion.")


if __name__ == "__main__":
    unittest.main()
