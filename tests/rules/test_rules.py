import pytest
from unittest.mock import patch, MagicMock
from src.rules.rules import RulesEngine

class TestRulesEngine:
    @patch('src.rules.rules.QARules')
    @patch('src.rules.rules.FinancialRules')
    def test_apply_rules_qa_answer_found(self, MockFinancialRules, MockQARules):
        # Arrange
        question = "What is your name?"
        expected_answer = "My name is Chatbot."

        # Set up mock for QARules
        mock_qa_instance = MockQARules.return_value
        mock_qa_instance.get_qa_answer.return_value = expected_answer
        
        # Create the RulesEngine instance
        rules_engine = RulesEngine()

        # Act
        answer = rules_engine.apply_rules(question)

        # Assert
        assert answer == expected_answer
        mock_qa_instance.get_qa_answer.assert_called_once_with(question)

    @patch('src.rules.rules.QARules')
    @patch('src.rules.rules.FinancialRules')
    def test_apply_rules_financial_question(self, MockFinancialRules, MockQARules):
        # Arrange
        question = "What is the total revenue of Microsoft in 2023?"
        expected_revenue = "$200 billion"

        # Set up mocks
        mock_qa_instance = MockQARules.return_value
        mock_qa_instance.get_qa_answer.return_value = "Sorry, I couldn't find an answer to your question."

        mock_financial_instance = MockFinancialRules.return_value
        mock_financial_instance.get_revenue.return_value = expected_revenue

        # Create the RulesEngine instance
        rules_engine = RulesEngine()

        # Act
        answer = rules_engine.apply_rules(question)

        # Assert
        assert answer == expected_revenue
        mock_financial_instance.get_revenue.assert_called_once_with('Microsoft', 2023)

    @patch('src.rules.rules.QARules')
    @patch('src.rules.rules.FinancialRules')
    def test_apply_rules_no_answer(self, MockFinancialRules, MockQARules):
        # Arrange
        question = "What is the total assets of Microsoft in 2021?"
        
        # Set up mocks
        mock_qa_instance = MockQARules.return_value
        mock_qa_instance.get_qa_answer.return_value = "Sorry, I couldn't find an answer to your question."

        mock_financial_instance = MockFinancialRules.return_value
        mock_financial_instance.get_total_assets.return_value = None

        # Create the RulesEngine instance
        rules_engine = RulesEngine()

        # Act
        answer = rules_engine.apply_rules(question)

        # Assert
        assert answer == "Sorry, I couldn't find an answer to your question."

    # Add more tests for different conditions here...

