import pytest
from unittest.mock import patch
from src.rules.financial_rules import FinancialRules

@pytest.fixture
def financial_rules():
    """Fixture to create FinancialRules instance"""
    return FinancialRules()

def test_get_revenue_success(financial_rules):
    """Test successful retrieval of revenue"""
    with patch('src.data_access.financial_data.financial_data_access.get_financial_data') as mock_get_data:
        mock_get_data.return_value = {'total_revenue': 1000000, 'net_income': 500000, 'total_assets': 2000000, 'total_liabilities': 1500000, 'cash_flow_from_operating_activities': 250000}
        result = financial_rules.get_revenue("Test Company", 2021)
        assert result == "The total revenue for Test Company in 2021 is 1000000 million.", "Failed to fetch correct revenue"

def test_get_revenue_no_data(financial_rules):
    """Test when no revenue data is available"""
    with patch('src.data_access.financial_data.financial_data_access.get_financial_data') as mock_get_data:
        mock_get_data.return_value = None
        result = financial_rules.get_revenue("Test Company", 2021)
        assert result == "Data not available.", "Failed to handle no data case"

def test_get_net_income_success(financial_rules):
    """Test successful retrieval of net income"""
    with patch('src.data_access.financial_data.financial_data_access.get_financial_data') as mock_get_data:
        mock_get_data.return_value = {'total_revenue': 1000000, 'net_income': 500000, 'total_assets': 2000000, 'total_liabilities': 1500000, 'cash_flow_from_operating_activities': 250000}
        result = financial_rules.get_net_income("Test Company", 2021)
        assert result == "The net income for Test Company in 2021 is 500000 million.", "Failed to fetch correct net income"

def test_get_total_assets_success(financial_rules):
    """Test successful retrieval of total assets"""
    with patch('src.data_access.financial_data.financial_data_access.get_financial_data') as mock_get_data:
        mock_get_data.return_value = {'total_revenue': 1000000, 'net_income': 500000, 'total_assets': 2000000, 'total_liabilities': 1500000, 'cash_flow_from_operating_activities': 250000}
        result = financial_rules.get_total_assets("Test Company", 2021)
        assert result == "The total assets for Test Company in 2021 are 2000000 million.", "Failed to fetch correct total assets"

def test_get_total_liabilities_success(financial_rules):
    """Test successful retrieval of total liabilities"""
    with patch('src.data_access.financial_data.financial_data_access.get_financial_data') as mock_get_data:
        mock_get_data.return_value = {'total_revenue': 1000000, 'net_income': 500000, 'total_assets': 2000000, 'total_liabilities': 1500000, 'cash_flow_from_operating_activities': 250000}
        result = financial_rules.get_total_liabilities("Test Company", 2021)
        assert result == "The total liabilities for Test Company in 2021 are 1500000 million.", "Failed to fetch correct total liabilities"

def test_get_cash_flow_success(financial_rules):
    """Test successful retrieval of cash flow"""
    with patch('src.data_access.financial_data.financial_data_access.get_financial_data') as mock_get_data:
        mock_get_data.return_value = {'total_revenue': 1000000, 'net_income': 500000, 'total_assets': 2000000, 'total_liabilities': 1500000, 'cash_flow_from_operating_activities': 250000}
        result = financial_rules.get_cash_flow("Test Company", 2021)
        assert result == "The cash flow from operating activities for Test Company in 2021 is 250000 million.", "Failed to fetch correct cash flow"

def test_get_percentage_change_in_net_income_success(financial_rules):
    """Test successful calculation of percentage change in net income"""
    with patch('src.data_access.financial_data.financial_data_access.get_financial_data') as mock_get_data:
        mock_get_data.side_effect = [
            {'total_revenue': 1000000, 'net_income': 500000, 'total_assets': 2000000, 'total_liabilities': 1500000, 'cash_flow_from_operating_activities': 250000},  # Start year data
            {'total_revenue': 1200000, 'net_income': 600000, 'total_assets': 2200000, 'total_liabilities': 1600000, 'cash_flow_from_operating_activities': 260000}   # End year data
        ]
        result = financial_rules.get_percentage_change_in_net_income("Test Company", 2020, 2021)
        assert result == "The percentage change in net income for Test Company from 2020 to 2021 is 20.0%.", "Failed to calculate correct percentage change"

def test_get_percentage_change_in_net_income_no_data(financial_rules):
    """Test handling of no data for percentage change calculation"""
    with patch('src.data_access.financial_data.financial_data_access.get_financial_data') as mock_get_data:
        mock_get_data.side_effect = [None, None]  # No data for both years
        result = financial_rules.get_percentage_change_in_net_income("Test Company", 2020, 2021)
        assert result == "Data not available.", "Failed to handle no data case"
