import pytest
from unittest.mock import patch
from src.main import get_answer

def test_get_answer_with_known_qa_pair():
    with patch('data_access.qa_pairs.qa_data_access.get_qa_pair') as mock_get_qa_pair:
        mock_get_qa_pair.return_value = "Some predefined answer."
        question = "What is the capital of France?"
        answer = get_answer(question)
        assert answer == "Some predefined answer."
        mock_get_qa_pair.assert_called_once_with(question)

def test_get_answer_with_financial_data():
    with patch('data_access.qa_pairs.qa_data_access.get_qa_pair', return_value=None), \
         patch('data_access.financial_data.financial_data_access.get_financial_data') as mock_get_financial_data:
        
        mock_get_financial_data.return_value = [1000]  # Mocking the financial data response
        question = "What is the total revenue for Microsoft in 2023?"
        answer = get_answer(question)
        assert answer == "The total revenue for Microsoft in 2023 is 1000 million."
        mock_get_financial_data.assert_called_once_with('Microsoft', 2023)

def test_get_answer_with_no_financial_data():
    with patch('data_access.qa_pairs.qa_data_access.get_qa_pair', return_value=None), \
         patch('data_access.financial_data.financial_data_access.get_financial_data') as mock_get_financial_data:
        
        mock_get_financial_data.return_value = None  # Simulating no financial data
        question = "What is the total revenue for Microsoft in 2023?"
        answer = get_answer(question)
        assert answer == "No financial data available for Microsoft in 2023."
        mock_get_financial_data.assert_called_once_with('Microsoft', 2023)

def test_get_answer_with_unknown_question():
    with patch('data_access.qa_pairs.qa_data_access.get_qa_pair', return_value=None):
        question = "What is the weather today?"
        answer = get_answer(question)
        assert answer == "Sorry, I couldn't find an answer to your question."
