import psycopg2
from config import DB_CONFIG
from typing import List, Tuple

class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass

class FinancialDataInserter:
    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.financial_data: List[Tuple] = [
            ('Microsoft', 2023, 211915, 72361, 411976, 205753, None),
            ('Microsoft', 2022, 198270, 72738, 364840, 198298, None),
            ('Microsoft', 2021, 168088, 61271, 333779, 191791, None),
            ('Tesla', 2023, 96773, 14974, 106618, 43009, None),
            ('Tesla', 2022, 81462, 12587, 82338, 36440, None),
            ('Tesla', 2021, 53823, 5644, 62131, 30548, None),
            ('Apple', 2023, 383285, 96995, 352583, 290437, None),
            ('Apple', 2022, 394328, 99803, 352755, 302038, None),
            ('Apple', 2021, 365817, 94680, 351002, 287912, None)
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
                    # Replace None with 0 for the cash flow column
                    self.financial_data = [
                        (
                            company_name, year, total_revenue, net_income,
                            total_assets, total_liabilities,
                            cash_flow_from_operating_activities if cash_flow_from_operating_activities is not None else 0
                        )
                        for (company_name, year, total_revenue, net_income,
                             total_assets, total_liabilities,
                             cash_flow_from_operating_activities)
                        in self.financial_data
                    ]
                    
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
                    cur.executemany(insert_query, self.financial_data)
                    conn.commit()
                    print("Financial data inserted/updated successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
            if conn is not None:
                conn.rollback()

# Instantiate with dependency injection
financial_data_inserter = FinancialDataInserter(DB_CONFIG)

if __name__ == "__main__":
    financial_data_inserter.insert_financial_data()
