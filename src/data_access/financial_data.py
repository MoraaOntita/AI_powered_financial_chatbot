import psycopg2
from config import DB_CONFIG
from typing import Optional, Tuple, List, Dict
import logging

# Set up logging
logger = logging.getLogger('BCGChatbotLogger')

class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass

class FinancialDataAccess:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _connect(self):
        """Establishes a connection to the database."""
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise DatabaseError("Database connection error.")

    def _fetchone(self, query: str, params: Tuple) -> Optional[Dict]:
        """Executes a query and fetches one result."""
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    result = cur.fetchone()
                    return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to fetch one record: {e}")
            raise DatabaseError("Failed to fetch data.")

    def _fetchall(self, query: str, params: Tuple) -> List[Dict]:
        """Executes a query and fetches all results."""
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    results = cur.fetchall()
                    return [dict(result) for result in results]
        except Exception as e:
            logger.error(f"Failed to fetch all records: {e}")
            raise DatabaseError("Failed to fetch data.")

    def get_financial_data(self, company_name: str, year: int) -> Optional[Dict]:
        """Fetches financial data for a specific company and year."""
        query = """
        SELECT total_revenue, net_income, total_assets, total_liabilities, cash_flow_from_operating_activities
        FROM financial_data
        WHERE company_name = %s AND year = %s
        """
        return self._fetchone(query, (company_name, year))

    def get_qa_pairs(self, company_name: str, year: int) -> List[Dict]:
        """Fetches QA pairs for a specific company and year."""
        query = """
        SELECT question, answer
        FROM qa_pairs
        WHERE company_name = %s AND year = %s
        """
        return self._fetchall(query, (company_name, year))

# Instantiate with dependency injection
financial_data_access = FinancialDataAccess(DB_CONFIG)
