FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file from the parent directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY .. .

# Command to run tests
CMD ["pytest", "tests/"]  # This is optional since you override it in docker-compose
