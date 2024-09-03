import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configuration
DATABASE_URL = 'postgresql://user:password@localhost/dbname'
DATA_FILE = '/home/moraa/Documents/BCG-Chatbot/data/BCG-X - Sheet1.csv'

def insert_financial_data(data_file: str, db_url: str):
    try:
        # Read CSV data
        df = pd.read_csv(data_file)
        
        # Replace NaN values with zero for 'cash_flow_operating'
        df['Cash Flow from Operating Activities'].fillna(0, inplace=True)
        
        # Connect to the database
        engine = create_engine(db_url)
        with engine.connect() as connection:
            for _, row in df.iterrows():
                # Prepare data
                data = {
                    'company_name': row.get('Company Name'),
                    'year': row.get('Year'),
                    'total_revenue': row.get('Total Revenue'),
                    'net_income': row.get('Net Income'),
                    'total_assets': row.get('Total Assets'),
                    'total_liabilities': row.get('Total Liabilities'),
                    'cash_flow_operating': row.get('Cash Flow from Operating Activities'),
                }
                
                # Insert or update data
                connection.execute("""
                    INSERT INTO financial_data (company_name, year, total_revenue, net_income, total_assets, total_liabilities, cash_flow_operating)
                    VALUES (%(company_name)s, %(year)s, %(total_revenue)s, %(net_income)s, %(total_assets)s, %(total_liabilities)s, %(cash_flow_operating)s)
                    ON CONFLICT (company_name, year)
                    DO UPDATE SET
                        total_revenue = EXCLUDED.total_revenue,
                        net_income = EXCLUDED.net_income,
                        total_assets = EXCLUDED.total_assets,
                        total_liabilities = EXCLUDED.total_liabilities,
                        cash_flow_operating = EXCLUDED.cash_flow_operating;
                """, data)
                
            print("Financial data inserted/updated successfully!")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    insert_financial_data(DATA_FILE, DATABASE_URL)
