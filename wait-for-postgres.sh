#!/bin/bash

set -e

# Check if the necessary environment variables are set
if [[ -z "$POSTGRES_USER" || -z "$POSTGRES_PASSWORD" || -z "$POSTGRES_DB" ]]; then
  echo "Error: Required environment variables (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB) are not set."
  exit 1
fi

host="$1"
shift  # This removes the host argument
cmd="$@"  # This captures the remaining arguments as the command

# Set PGPASSWORD environment variable
export PGPASSWORD="$POSTGRES_PASSWORD"

# Wait until PostgreSQL is up
echo "Waiting for PostgreSQL to be ready at $host..."
for i in {1..10}; do  # Retry up to 10 times
  if psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; then
    >&2 echo "Postgres is up - executing command"
    if [[ -n "$cmd" ]]; then
      exec "$cmd"
    else
      echo "No command provided to execute."
      exit 1
    fi
  fi
  >&2 echo "Postgres is unavailable - sleeping (attempt $i)"
  sleep 2  # Adjust sleep time between retries if needed
done

>&2 echo "Error: PostgreSQL did not become available in time."
exit 1
