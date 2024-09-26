import pytest
import os
import sys
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock

# Ensure the src directory is in the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.inserting_data.insert_qa_pairs import QADataInserter, DatabaseError

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
def qa_data_inserter():
    """Fixture to create QADataInserter with test DB config"""
    return QADataInserter(DB_CONFIG)

def test_create_table_success(qa_data_inserter):
    """Test successful table creation"""
    with patch.object(qa_data_inserter, '_connect', return_value=MagicMock()):
        try:
            qa_data_inserter._create_table()
        except DatabaseError:
            pytest.fail("DatabaseError raised during table creation")

def test_insert_qa_pairs_success(qa_data_inserter):
    """Test successful QA pairs insertion"""
    with patch.object(qa_data_inserter, '_connect', return_value=MagicMock()):
        try:
            qa_data_inserter.insert_qa_pairs()
        except Exception as e:
            pytest.fail(f"An error occurred: {e}")

def test_insert_qa_pairs_with_invalid_db_config():
    """Test insertion with invalid DB config raises DatabaseError"""
    invalid_db_config = {'dbname': 'invalid_db'}
    inserter = QADataInserter(invalid_db_config)
    
    # Mock both _create_table and _connect methods to simulate failure
    with patch.object(inserter, '_create_table', return_value=None):
        with patch.object(inserter, '_connect', side_effect=DatabaseError("Failed to connect to the database")):
            with pytest.raises(DatabaseError):
                inserter.insert_qa_pairs()
