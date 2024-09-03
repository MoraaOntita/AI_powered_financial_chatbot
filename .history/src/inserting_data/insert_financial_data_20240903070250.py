import psycopg2
from config import DB_CONFIG
from typing import List, Tuple

class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass

class FinancialDataInserter:
    def __init__(self, db_config: dict):
        self.db_config = db_config
        # Updated data with possible NULL values replaced by 0
        self.financial_data: List[Tuple] = [
            ('Microsoft', 2023, 211915, 72361, 411976, 205753, 34704),
            ('Microsoft', 2022, 198270, 72738, 364840, 198298, 13931),
            ('Microsoft', 2021, 168088, 61271, 333779, 191791, 14224),
            ('Tesla', 2023, 96773, 14974, 106618, 43009, 8891),
            ('Tesla', 2022, 81462, 12587, 82338, 36440, 13656),
            ('Tesla', 2021, 53823, 5644, 62131, 30548, 6523),
            ('Apple', 2023, 383285, 96995, 352583, 290437, 110543),
            ('Apple', 2022, 394328, 99803, 352755, 302038, 122151),
            ('Apple', 2021, 365817, 94680, 351002, 287912, 104038)
        ]

    def _connect(self):
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            raise DatabaseError(f"Failed to connect to the database: {e}")

    def insert_financial_data(self):
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    insert_query = """
                    INSERT INTO financial_data (company_name, year, total_revenue, net_income, total_assets, total_liabilities, cash_flow_from_operating_activities)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (company_name, year) 
                    DO UPDATE SET 
                        total_revenue = EXCLUDED.total_revenue,
                        net_income = EXCLUDED.net_income,
                        total_assets = EXCLUDED.total_assets,
                        total_liabilities = EXCLUDED.total_liabilities,
                        cash_flow_from_operating_activities = EXCLUDED.cash_flow_from_operating_activities;
                    """
                    # Replace null values with 0 before executing the query
                    data_with_no_nulls = self._replace_null_values(self.financial_data)
                    cur.executemany(insert_query, data_with_no_nulls)
                    conn.commit()
                    print("Financial data inserted/updated successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
            if conn is not None:
                conn.rollback()

    def _replace_null_values(self, data: List[Tuple]) -> List[Tuple]:
        """Replace None values with 0 in financial data."""
        return [
            tuple(0 if val is None else val for val in row)
            for row in data
        ]

# Instantiate with dependency injection
financial_data_inserter = FinancialDataInserter(DB_CONFIG)

if __name__ == "__main__":
    financial_data_inserter.insert_financial_data()
