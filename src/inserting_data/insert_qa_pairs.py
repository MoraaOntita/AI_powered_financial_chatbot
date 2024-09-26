import psycopg2
from config import DB_CONFIG
from typing import List, Tuple

class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass

class QADataInserter:
    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.qa_pairs: List[Tuple] = [
            ('What is the total revenue for Microsoft in 2023?', 'The total revenue for Microsoft in 2023 is $211,915 million.', 'Microsoft', 2023),
            ('What is the net income for Tesla in 2022?', 'The net income for Tesla in 2022 is $12,587 million.', 'Tesla', 2022),
            ('How has net income changed for Apple from 2021 to 2022?', 'The net income for Apple changed from $94,680 million in 2021 to $99,803 million in 2022, an increase of $5,123 million.', 'Apple', 2022),
            ('What are the total assets for Microsoft in 2023?', 'The total assets for Microsoft in 2023 are $411,976 million.', 'Microsoft', 2023),
            ('What are the total liabilities for Tesla in 2023?', 'The total liabilities for Tesla in 2023 are $43,009 million.', 'Tesla', 2023),
            ('What is the cash flow from operating activities for Apple in 2022?', 'The cash flow from operating activities for Apple in 2022 is $122,151 million.', 'Apple', 2022),
            ('How has total revenue changed for Tesla from 2021 to 2022?', 'The total revenue for Tesla changed from $53,823 million in 2021 to $81,462 million in 2022, an increase of $27,639 million.', 'Tesla', 2022),
            ('What was the total revenue of Apple for the last year available?', 'The total revenue of Apple for the last year available is $383,285 million (2023).', 'Apple', 2023),
            ('Which company had the highest net income in 2023?', 'The company with the highest net income in 2023 was Apple with a net income of $96,995 million.', 'Apple', 2023),
            ('What is the percentage change in net income for Microsoft from 2021 to 2022?', 'The percentage change in net income for Microsoft from 2021 to 2022 is 18.7%.', 'Microsoft', 2022)
        ]

    def _connect(self):
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            raise DatabaseError(f"Failed to connect to the database: {e}")

    def _create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS qa_pairs (
            id SERIAL PRIMARY KEY,
            question TEXT,
            answer TEXT,
            company_name VARCHAR(255),
            year INT,
            UNIQUE (question, company_name, year)
        );
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()

    def insert_qa_pairs(self):
        conn = None  # Initialize conn to None
        try:
            self._create_table()
            conn = self._connect()  # Attempt to connect
            with conn.cursor() as cur:
                insert_query = """
                INSERT INTO qa_pairs (question, answer, company_name, year)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (question, company_name, year) 
                DO UPDATE SET 
                    answer = EXCLUDED.answer;
                """
                cur.executemany(insert_query, self.qa_pairs)
                conn.commit()
                print("QA pairs inserted/updated successfully!")
        except DatabaseError as e:
            print(f"An error occurred: {e}")
            raise  # Re-raise the DatabaseError for the test to catch
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            if conn is not None:  # Only attempt to rollback if conn is not None
                conn.rollback()

# Instantiate with dependency injection
qa_data_inserter = QADataInserter(DB_CONFIG)

if __name__ == "__main__":
    qa_data_inserter.insert_qa_pairs()
