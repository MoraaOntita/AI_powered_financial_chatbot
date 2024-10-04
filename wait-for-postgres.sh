#!/bin/bash

set -e

# Check if the necessary environment variables are set
if [[ -z "$POSTGRES_USER" || -z "$POSTGRES_PASSWORD" || -z "$POSTGRES_DB" ]]; then
  echo "Error: Required environment variables (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB) are not set."
  exit 1
fi

host="$1"
shift
cmd="$@"

# Set PGPASSWORD environment variable
export PGPASSWORD="$POSTGRES_PASSWORD"

# Wait until PostgreSQL is up
echo "Waiting for PostgreSQL to be ready at $host..."
for i in {1..10}; do  # Retry up to 10 times
  if psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; then
    >&2 echo "Postgres is up - executing command"
    if [[ "$cmd" == "run_scripts" ]]; then
      run_scripts
    else
      exec "$cmd"
    fi
    exit 0
  fi
  >&2 echo "Postgres is unavailable - sleeping (attempt $i)"
  sleep 2  # Adjust sleep time between retries if needed
done

>&2 echo "Error: PostgreSQL did not become available in time."
exit 1
