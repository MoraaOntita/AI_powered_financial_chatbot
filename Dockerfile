# Use a Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Ensure the target directory exists
RUN mkdir -p /app/data

# Copy the data file into the container with the new name
COPY data/BCG_X_Sheet1.csv /app/data/BCG_X_Sheet1.csv

# Copy the wait-for-postgres script
COPY wait-for-postgres.sh /app/wait-for-postgres.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/wait-for-postgres.sh

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 5000

# Define the entry point for the container
ENTRYPOINT ["/app/entrypoint.sh"]
