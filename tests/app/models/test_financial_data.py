import pytest
from unittest import mock
from psycopg2 import Error as Psycopg2Error
from app.models.financial_data import FinancialDataAccess, DatabaseError

# Mock data returned from the database
MOCK_FINANCIAL_DATA = {
    'total_revenue': 100000,
    'net_income': 50000,
    'total_assets': 150000,
    'total_liabilities': 80000,
    'cash_flow_from_operating_activities': 30000
}

@pytest.fixture
def mock_db_config():
    return {
        'dbname': 'test_db',
        'user': 'test_user',
        'password': 'test_pass',
        'host': 'postgres',
        'port': 5432
    }

@pytest.fixture
def financial_data_access(mock_db_config):
    return FinancialDataAccess(mock_db_config)

def test_get_financial_data_success(financial_data_access):
    """Test successful fetching of financial data."""
    company_name = "Test Company"
    year = 2021

    # Mock the _fetchone method to return our mock financial data
    with mock.patch.object(financial_data_access, '_fetchone', return_value=(
        MOCK_FINANCIAL_DATA['total_revenue'],
        MOCK_FINANCIAL_DATA['net_income'],
        MOCK_FINANCIAL_DATA['total_assets'],
        MOCK_FINANCIAL_DATA['total_liabilities'],
        MOCK_FINANCIAL_DATA['cash_flow_from_operating_activities']
    )):
        result = financial_data_access.get_financial_data(company_name, year)

        assert result == MOCK_FINANCIAL_DATA
        financial_data_access._fetchone.assert_called_once_with(
            """
            SELECT total_revenue, net_income, total_assets, total_liabilities, cash_flow_from_operating_activities
            FROM financial_data
            WHERE company_name = %s AND year = %s
            """.strip(), (company_name, year)
        )
def test_get_financial_data_no_result(financial_data_access):
    """Test fetching financial data when no result is found."""
    company_name = "Nonexistent Company"
    year = 2021

    # Mock the _fetchone method to return None
    with mock.patch.object(financial_data_access, '_fetchone', return_value=None):
        result = financial_data_access.get_financial_data(company_name, year)

        assert result is None
        financial_data_access._fetchone.assert_called_once_with(
            """
            SELECT total_revenue, net_income, total_assets, total_liabilities, cash_flow_from_operating_activities
            FROM financial_data
            WHERE company_name = %s AND year = %s
            """.strip(), (company_name, year)
        )

def test_database_connection_error(financial_data_access):
    """Test handling of a database connection error."""
    with mock.patch('psycopg2.connect', side_effect=Psycopg2Error("Connection failed")):
        with pytest.raises(DatabaseError, match="Failed to connect to the database: Connection failed"):
            financial_data_access._connect()

def test_query_execution_error(financial_data_access):
    """Test handling of a query execution error."""
    company_name = "Test Company"
    year = 2021

    # Mock the _fetchone method to raise an exception
    with mock.patch.object(financial_data_access, '_fetchone', side_effect=Psycopg2Error("Query execution failed")):
        with pytest.raises(DatabaseError, match="Query execution failed"):
            financial_data_access.get_financial_data(company_name, year)
