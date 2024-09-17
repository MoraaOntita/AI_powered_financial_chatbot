import psycopg2
from config import DB_CONFIG

try:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # Test connection and query
            query = "SELECT answer FROM qa_pairs WHERE question = %s"
            question = 'What are the total assets for Microsoft in 2023?'
            cur.execute(query, (question,))
            result = cur.fetchone()
            print(f"Query result: {result}")
except Exception as e:
    print(f"An error occurred: {e}")
