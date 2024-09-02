import psycopg2
from config import DB_CONFIG
from typing import Optional

class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass

class QADataAccess:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _connect(self):
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            raise DatabaseError(f"Failed to connect to the database: {e}")

    def _fetchone(self, query: str, params: tuple) -> Optional[tuple]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()

    def get_qa_pair(self, question: str) -> str:
        query = """
        SELECT answer FROM qa_pairs WHERE question = %s
        """
        result = self._fetchone(query, (question,))
        if result:
            return result[0]
        else:
            return "Sorry, I don't know the answer to that question."

# Instantiate with dependency injection
qa_data_access = QADataAccess(DB_CONFIG)