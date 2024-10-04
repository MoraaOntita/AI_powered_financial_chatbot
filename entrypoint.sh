#!/bin/bash

# Load environment variables from .env file
set -a
source /app/.env
set +a

# Wait for PostgreSQL to be ready and then run the data insertion scripts and start Flask
/app/wait-for-postgres.sh postgres bash -c "
  python /app/src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv &&
  python /app/src/inserting_data/insert_qa_pairs.py &&
  flask run --host=0.0.0.0 --port=5000
"
