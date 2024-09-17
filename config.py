import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': 'postgres',
    'port': 5432           
}
