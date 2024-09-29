import psycopg2
from config import DB_CONFIG
from typing import Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass

class FinancialDataAccess:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _connect(self):
        try:
            return psycopg2.connect(**self.db_config)
        except psycopg2.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise DatabaseError(f"Failed to connect to the database: {e}")

    def _fetchone(self, query: str, params: Tuple):
        with self._connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()

    def get_financial_data(self, company_name: str, year: int) -> Optional[dict]:
        query = """
            SELECT total_revenue, net_income, total_assets, total_liabilities, cash_flow_from_operating_activities
            FROM financial_data
            WHERE company_name = %s AND year = %s
        """.strip()
        try:
            result = self._fetchone(query, (company_name, year))
            if result is not None:
                return {
                    'total_revenue': result[0],
                    'net_income': result[1],
                    'total_assets': result[2],
                    'total_liabilities': result[3],
                    'cash_flow_from_operating_activities': result[4],
                }
            return None
        except psycopg2.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise DatabaseError(f"Failed to execute query: {e}")
