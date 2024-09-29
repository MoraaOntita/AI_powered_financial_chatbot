import pytest
import os
import sys
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock

# Ensure the src directory is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.data_access.qa_pairs import QADataAccess, DatabaseError

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
def qa_data_access():
    """Fixture to create QADataAccess with test DB config"""
    return QADataAccess(DB_CONFIG)

def test_get_qa_pair_success(qa_data_access):
    """Test successful fetching of a QA pair"""
    mock_result = ('This is a mock answer.',)
    with patch.object(qa_data_access, '_fetchone', return_value=mock_result):
        result = qa_data_access.get_qa_pair("Test Question")
        assert result == "This is a mock answer."

def test_get_qa_pair_no_result(qa_data_access):
    """Test fetching a QA pair when no result is found"""
    with patch.object(qa_data_access, '_fetchone', return_value=None):
        result = qa_data_access.get_qa_pair("Unknown Question")
        assert result == "Sorry, I don't know the answer to that question."

def test_db_connection_failure(qa_data_access):
    """Test database connection failure"""
    with patch.object(qa_data_access, '_connect', side_effect=DatabaseError("Failed to connect to the database")):
        with pytest.raises(DatabaseError):
            qa_data_access.get_qa_pair("Test Question")
