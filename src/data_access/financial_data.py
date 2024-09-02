import psycopg2
from config import DB_CONFIG
from typing import Optional, Tuple, List

class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass

class FinancialDataAccess:
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def _connect(self):
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            raise DatabaseError(f"Failed to connect to the database: {e}")

    def _fetchone(self, query: str, params: Tuple) -> Optional[Tuple]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()

    def _fetchall(self, query: str, params: Tuple) -> List[Tuple]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()

    def get_financial_data(self, company_name: str, year: int) -> Optional[Tuple]:
        query = """
        SELECT total_revenue, net_income, total_assets, total_liabilities, cash_flow_from_operating_activities
        FROM financial_data
        WHERE company_name = %s AND year = %s
        """
        return self._fetchone(query, (company_name, year))

    def get_qa_pairs(self, company_name: str, year: int) -> List[Tuple]:
        query = """
        SELECT question, answer
        FROM qa_pairs
        WHERE company_name = %s AND year = %s
        """
        return self._fetchall(query, (company_name, year))

# Instantiate with dependency injection
financial_data_access = FinancialDataAccess(DB_CONFIG)
