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
            logger.error(f"Database connection error: {e}")
            raise DatabaseError(f"Failed to connect to the database: {e}")

    def _fetchone(self, query: str, params: Tuple) -> Optional[dict]:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    row = cur.fetchone()
                    if row:
                        return {
                            'total_revenue': row[0],
                            'net_income': row[1],
                            'total_assets': row[2],
                            'total_liabilities': row[3],
                            'cash_flow_from_operating_activities': row[4]
                        }
                    return None
        except psycopg2.Error as e:
            logger.error(f"Query execution error: {e}")
            raise DatabaseError(f"Failed to execute query: {e}")

    def get_financial_data(self, company_name: str, year: int) -> Optional[dict]:
        query = """
        SELECT total_revenue, net_income, total_assets, total_liabilities, cash_flow_from_operating_activities
        FROM financial_data
        WHERE company_name = %s AND year = %s
        """
        return self._fetchone(query, (company_name, year))
