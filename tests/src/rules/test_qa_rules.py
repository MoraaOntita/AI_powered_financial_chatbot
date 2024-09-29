import pytest
from unittest.mock import patch
from src.rules.qa_rules import QARules

class TestQARules:
    @patch('src.data_access.qa_pairs.QADataAccess.get_qa_pair')
    def test_get_qa_answer_found(self, mock_get_qa_pair):
        # Arrange
        question = "What is your name?"
        expected_answer = "My name is Chatbot."

        # Mock the return value of get_qa_pair
        mock_get_qa_pair.return_value = expected_answer
        
        qa_rules = QARules()

        # Act
        answer = qa_rules.get_qa_answer(question)

        # Assert
        assert answer == expected_answer
        mock_get_qa_pair.assert_called_once_with(question)

    @patch('src.data_access.qa_pairs.QADataAccess.get_qa_pair')
    def test_get_qa_answer_not_found(self, mock_get_qa_pair):
        # Arrange
        question = "What is the capital of France?"

        # Mock the return value of get_qa_pair to None
        mock_get_qa_pair.return_value = None  

        qa_rules = QARules()

        # Act
        answer = qa_rules.get_qa_answer(question)

        # Assert
        assert answer == "Sorry, I couldn't find an answer to your question."
        mock_get_qa_pair.assert_called_once_with(question)
