# Variables
DOCKER = docker
DOCKER_COMPOSE = docker-compose

# Default target
all: build up test

# Build the Docker images
build:
	$(DOCKER_COMPOSE) build

# Start the services defined in docker-compose.yml
up:
	$(DOCKER_COMPOSE) up -d

# Stop and remove containers, networks, and volumes
down:
	$(DOCKER_COMPOSE) down

# Run the insert data scripts
insert-data:
	$(DOCKER_COMPOSE) exec backend python src/inserting_data/insert_financial_data.py --data-file /app/data/BCG_X_Sheet1.csv
	$(DOCKER_COMPOSE) exec backend python src/inserting_data/insert_qa_pairs.py

# Run tests inside the backend container
test:
	$(DOCKER_COMPOSE) exec backend pytest

# Lint code inside the backend container
lint:
	$(DOCKER_COMPOSE) exec backend pylint src

# Format code inside the backend container
format:
	$(DOCKER_COMPOSE) exec backend black src

# Check if the application is running correctly
check:
	$(DOCKER_COMPOSE) exec backend curl -X POST -H "Content-Type: application/json" -d '{"question": "What is Microsoft's revenue for 2023?"}' http://localhost:5000/ask

# Clean up temporary files and volumes
clean:
	$(DOCKER_COMPOSE) down -v
	rm -rf .tox .nox .coverage coverage.xml

# Help command to display available commands
help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  all           - Build, start containers, and run tests"
	@echo "  build         - Build the Docker images"
	@echo "  up            - Start the services"
	@echo "  down          - Stop and remove containers, networks, and volumes"
	@echo "  insert-data   - Run data insertion scripts"
	@echo "  test          - Run tests inside the backend container"
	@echo "  lint          - Lint code inside the backend container"
	@echo "  format        - Format code inside the backend container"
	@echo "  check         - Check if the application responds correctly"
	@echo "  clean         - Clean up temporary files and volumes"
	@echo "  help          - Display this help message"

# Phony targets
.PHONY: all build up down insert-data test lint format check clean help
