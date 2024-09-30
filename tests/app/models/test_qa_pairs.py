import pytest
from unittest.mock import patch, MagicMock
from app.models.qa_pairs import QADataAccess, DatabaseError  # Import DatabaseError

@pytest.fixture
def db_config():
    return {
        'dbname': 'BCG_Finance',
        'user': 'postgres',
        'password': 'Musy19',
        'host': 'localhost',
        'port': '5432'
    }

def test_get_qa_pair_success(db_config):
    qa_access = QADataAccess(db_config)
    question = "What is the capital of France?"
    
    # Mock the _fetchone method to return a specific answer
    with patch.object(qa_access, '_fetchone', return_value=("Paris",)):
        answer = qa_access.get_qa_pair(question)
        assert answer == "Paris"

def test_get_qa_pair_no_result(db_config):
    qa_access = QADataAccess(db_config)
    question = "What is the capital of Atlantis?"

    # Mock the _fetchone method to return None
    with patch.object(qa_access, '_fetchone', return_value=None):
        answer = qa_access.get_qa_pair(question)
        assert answer == "Sorry, I don't know the answer to that question."

def test_database_connection_error(db_config):
    qa_access = QADataAccess(db_config)

    # Mock the _connect method to raise a DatabaseError
    with patch.object(qa_access, '_connect', side_effect=DatabaseError("Connection error")):
        with pytest.raises(DatabaseError, match="Connection error"):
            qa_access._connect()

def test_query_execution_error(db_config):
    qa_access = QADataAccess(db_config)

    # Mock the _fetchone method to raise a DatabaseError
    with patch.object(qa_access, '_fetchone', side_effect=DatabaseError("Execution error")):
        with pytest.raises(DatabaseError, match="Execution error"):
            qa_access.get_qa_pair("Some question")
