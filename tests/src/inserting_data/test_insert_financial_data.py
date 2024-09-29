import pytest
import os
import sys
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock

# Ensure the src directory is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.inserting_data.insert_financial_data import FinancialDataInserter, DatabaseError

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
def financial_data_inserter():
    """Fixture to create FinancialDataInserter with test DB config"""
    return FinancialDataInserter(DB_CONFIG)

def test_create_table_success(financial_data_inserter):
    """Test successful table creation"""
    with patch.object(financial_data_inserter, '_connect', return_value=MagicMock()):
        try:
            financial_data_inserter._create_table()
        except DatabaseError:
            pytest.fail("DatabaseError raised during table creation")

def test_insert_financial_data_success(financial_data_inserter):
    """Test successful financial data insertion"""
    with patch.object(financial_data_inserter, '_connect', return_value=MagicMock()):
        with patch.object(financial_data_inserter, '_create_table', return_value=None):
            try:
                financial_data_inserter.insert_financial_data()
            except Exception as e:
                pytest.fail(f"An error occurred: {e}")

def test_insert_financial_data_with_invalid_db_config():
    """Test insertion with invalid DB config raises DatabaseError"""
    invalid_db_config = {'dbname': 'invalid_db'}
    inserter = FinancialDataInserter(invalid_db_config)
    
    # Mock _create_table and _connect methods to simulate failure
    with patch.object(inserter, '_create_table', return_value=None):
        with patch.object(inserter, '_connect', side_effect=DatabaseError("Failed to connect to the database")):
            with pytest.raises(DatabaseError):
                inserter.insert_financial_data()
