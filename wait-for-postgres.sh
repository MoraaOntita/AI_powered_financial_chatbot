#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

# Set PGPASSWORD environment variable
export PGPASSWORD="$POSTGRES_PASSWORD"

# Wait until PostgreSQL is up
echo "Waiting for PostgreSQL to be ready..."
until psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 2  # Adjust sleep time between retries if needed
done

>&2 echo "Postgres is up - executing command"
exec "$cmd"
