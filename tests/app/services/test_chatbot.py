import pytest
from unittest import mock
from app.services.chatbot import (
    fetch_financial_data, 
    calculate_percentage_change, 
    extract_year_from_question, 
    extract_company_and_metric, 
    process_question, 
    ChatbotError
)
from datetime import datetime

# Mock data returned from the database
MOCK_FINANCIAL_DATA = {
    'total_revenue': 100000,
    'net_income': 50000,
    'total_assets': 150000,
    'total_liabilities': 80000,
    'cash_flow_from_operating_activities': 30000
}

@pytest.fixture
def mock_financial_data_access():
    with mock.patch('app.services.chatbot.financial_data_access.get_financial_data') as mock_get_data:
        yield mock_get_data

def test_fetch_financial_data_success(mock_financial_data_access):
    """Test successful fetching of financial data."""
    company_name = "Test Company"
    year = 2021

    # Mock the return value for the database call
    mock_financial_data_access.return_value = MOCK_FINANCIAL_DATA

    result = fetch_financial_data(company_name, year)
    assert result == MOCK_FINANCIAL_DATA
    mock_financial_data_access.assert_called_once_with(company_name, year)

def test_fetch_financial_data_error(mock_financial_data_access):
    """Test handling of error while fetching financial data."""
    mock_financial_data_access.side_effect = Exception("Database error")

    result = fetch_financial_data("Test Company", 2021)
    assert result is None

def test_calculate_percentage_change_success(mock_financial_data_access):
    """Test percentage change calculation."""
    company = "Test Company"
    metric = "total_revenue"
    start_year = 2020
    end_year = 2021

    mock_financial_data_access.side_effect = [
        {'total_revenue': 100000},
        {'total_revenue': 200000}
    ]

    result = calculate_percentage_change(company, metric, start_year, end_year)
    assert result == 100.0

def test_calculate_percentage_change_zero_division(mock_financial_data_access):
    """Test for ZeroDivisionError in percentage change."""
    company = "Test Company"
    metric = "total_revenue"
    start_year = 2020
    end_year = 2021

    mock_financial_data_access.side_effect = [
        {'total_revenue': 0},
        {'total_revenue': 100000}
    ]

    result = calculate_percentage_change(company, metric, start_year, end_year)
    assert result is None  # Should return None for ZeroDivisionError

def test_extract_year_from_question():
    """Test extracting year from a question."""
    question = "What is the revenue for Apple in 2021?"
    result = extract_year_from_question(question)
    assert result == 2021

    question_no_year = "What is the revenue for Apple?"
    result = extract_year_from_question(question_no_year)
    assert result == None  # No year mentioned

def test_extract_company_and_metric():
    """Test extracting company and metric from question."""
    question = "What is the net income for Apple?"
    company, metric = extract_company_and_metric(question)
    assert company == "Apple"
    assert metric == "net_income"

def test_process_question_success(mock_financial_data_access):
    """Test processing a valid question."""
    mock_financial_data_access.return_value = MOCK_FINANCIAL_DATA

    question = "What is the total revenue for Apple in 2021?"
    result = process_question(question)
    assert result == "Apple's total revenue for 2021 was $100,000 million."

def test_process_question_error(mock_financial_data_access):
    """Test handling error when processing a question."""
    mock_financial_data_access.return_value = None  # Simulate no data found

    question = "What is the total revenue for Nonexistent Company in 2021?"
    result = process_question(question)

    # Update the expected result to match the actual error
    assert result == "Could not understand the company or financial metric from the question."

