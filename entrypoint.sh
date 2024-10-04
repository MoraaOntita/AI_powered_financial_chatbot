#!/bin/bash

# Function to load environment variables from .env file
load_env() {
  if [ -f /app/.env ]; then
    echo "Loading environment variables from .env file"
    set -a
    source /app/.env
    set +a
  else
    echo "Error: .env file not found or is a directory!"
    exit 1
  fi
}

# Function to check if required files exist
check_files() {
  for file in "$@"; do
    if [ ! -f "$file" ]; then
      echo "Error: $file not found!"
      exit 1
    fi
  done
}

# Function to run the scripts and start Flask
run_scripts() {
  echo "Postgres is up - executing data insertion scripts and starting Flask"
  bash -c "
    python /app/src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv &&
    python /app/src/inserting_data/insert_qa_pairs.py &&
    flask run --host=0.0.0.0 --port=5000
  "
}

# Load environment variables
load_env

# Wait for PostgreSQL to be ready and pass the command to run
/app/wait-for-postgres.sh postgres

# Check for necessary files
check_files /app/src/inserting_data/insert_financial_data.py /app/src/inserting_data/insert_qa_pairs.py

# Run the scripts and start Flask
run_scripts
