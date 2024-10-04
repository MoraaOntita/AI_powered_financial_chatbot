#!/bin/bash

# Ensure that the .env file exists and is a file, not a directory
if [ ! -f /app/.env ]; then
  echo "Error: .env file not found or is a directory!"
  exit 1
else
  echo "Loading environment variables from .env file"
  set -a
  source /app/.env
  set +a
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
/app/wait-for-postgres.sh postgres

# Check if PostgreSQL is ready
if [ $? -ne 0 ]; then
  echo "PostgreSQL is not ready, exiting..."
  exit 1
fi

# Check if the required scripts exist
if [ ! -f /app/src/inserting_data/insert_financial_data.py ]; then
  echo "Error: insert_financial_data.py not found!"
  exit 1
fi

if [ ! -f /app/src/inserting_data/insert_qa_pairs.py ]; then
  echo "Error: insert_qa_pairs.py not found!"
  exit 1
fi

# Run the data insertion scripts
echo "Postgres is up - executing data insertion scripts"
python /app/src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv
if [ $? -ne 0 ]; then
  echo "Error executing insert_financial_data.py"
  exit 1
fi

python /app/src/inserting_data/insert_qa_pairs.py
if [ $? -ne 0 ]; then
  echo "Error executing insert_qa_pairs.py"
  exit 1
fi

# Start Flask
echo "Starting Flask"
flask run --host=0.0.0.0 --port=5000
if [ $? -ne 0 ]; then
  echo "Error starting Flask, exiting..."
  exit 1
fi
