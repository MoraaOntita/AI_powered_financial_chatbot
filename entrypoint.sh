#!/bin/bash

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

check_files() {
  for file in "$@"; do
    if [ ! -f "$file" ]; then
      echo "Error: $file not found!"
      exit 1
    fi
  done
}

run_scripts() {
  echo "Postgres is up - executing data insertion scripts and starting Flask"
  bash -c "
    python /app/src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv &&
    python /app/src/inserting_data/insert_qa_pairs.py &&
    flask run --host=0.0.0.0 --port=5000
  "
}

load_env
/app/wait-for-postgres.sh postgres run_scripts
check_files /app/src/inserting_data/insert_financial_data.py /app/src/inserting_data/insert_qa_pairs.py
