#!/bin/bash

# Wait for PostgreSQL to be ready
/app/wait-for-postgres.sh postgres

# Check if the wait was successful
if [ $? -ne 0 ]; then
  echo "PostgreSQL is not ready. Exiting."
  exit 1
fi

# Run the data insertion scripts
python src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv
python src/inserting_data/insert_qa_pairs.py

# Start the Flask application
exec flask run --host=0.0.0.0 --port=5000
