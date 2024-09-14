#!/bin/bash

# Wait for PostgreSQL to be ready
./wait-for-postgres.sh postgres "python src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv && python src/inserting_data/insert_qa_pairs.py && exec flask run --host=0.0.0.0 --port=5000"

# Run the data insertion scripts
python src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv
python src/inserting_data/insert_qa_pairs.py

# Start the Flask application
exec flask run --host=0.0.0.0 --port=5000
