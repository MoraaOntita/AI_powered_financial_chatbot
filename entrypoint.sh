#!/bin/bash

# Load environment variables from .env file
set -a
source /app/.env
set +a

# Wait for PostgreSQL to be ready
/app/wait-for-postgres.sh postgres 5432

echo "PostgreSQL is up. Running data insertion scripts..."

# Run the financial data insertion script
python /app/src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv
if [ $? -ne 0 ]; then
  echo "Financial data insertion failed. Exiting."
  exit 1
fi
echo "Financial data inserted successfully."

# Run the QA pairs insertion script
python /app/src/inserting_data/insert_qa_pairs.py
if [ $? -ne 0 ]; then
  echo "QA pairs data insertion failed. Exiting."
  exit 1
fi
echo "QA pairs inserted successfully."

# Start the Flask application
echo "Starting the Flask application..."
exec flask run --host=0.0.0.0 --port=5000
