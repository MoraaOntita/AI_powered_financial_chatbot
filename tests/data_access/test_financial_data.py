import pytest
import os
import sys
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock

# Ensure the src directory is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.data_access.financial_data import FinancialDataAccess, DatabaseError

# Load environment variables from the .env file
load_dotenv()

# Use environment variables for DB_CONFIG
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'default_db'),
    'user': os.getenv('POSTGRES_USER', 'default_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'default_password'),
    'host': os.getenv('POSTGRES_HOST', 'postgres'),  # Use 'postgres' for Docker
    'port': os.getenv('POSTGRES_PORT', '5432')
}

@pytest.fixture
def financial_data_access():
    """Fixture to create FinancialDataAccess with test DB config"""
    return FinancialDataAccess(DB_CONFIG)

def test_get_financial_data_success(financial_data_access):
    """Test successful retrieval of financial data"""
    with patch.object(financial_data_access, '_connect', return_value=MagicMock()):
        mock_data = {'total_revenue': 1000000, 'net_income': 500000}
        with patch.object(financial_data_access, '_fetchone', return_value=mock_data):
            result = financial_data_access.get_financial_data("Test Company", 2021)
            assert result == mock_data, "Failed to fetch correct financial data"

def test_get_qa_pairs_success(financial_data_access):
    """Test successful retrieval of QA pairs"""
    with patch.object(financial_data_access, '_connect', return_value=MagicMock()):
        mock_data = [{'question': 'What is revenue?', 'answer': '1000000'}]
        with patch.object(financial_data_access, '_fetchall', return_value=mock_data):
            result = financial_data_access.get_qa_pairs("Test Company", 2021)
            assert result == mock_data, "Failed to fetch correct QA pairs"

def test_db_connection_failure(financial_data_access):
    """Test that DatabaseError is raised when connection fails"""
    with patch.object(financial_data_access, '_connect', side_effect=DatabaseError("Failed to connect to the database")):
        with pytest.raises(DatabaseError):
            financial_data_access.get_financial_data("Test Company", 2021)
