# Variables
PYTHON = python3
PIP = pip
FLASK = flask
VENV = venv

# Paths to the scripts
FINANCIAL_SCRIPT = src/inserting_data/insert_financial_data.py
QA_PAIRS_SCRIPT = src/inserting_data/insert_qa_pairs.py
MAIN_SCRIPT = src/main.py
RULES_DIR = src/rules/
RULES_SCRIPT = src/rules.py

# Export PYTHONPATH to include the root directory of the project
export PYTHONPATH := $(shell pwd)

# Targets

# Default target
all: install run-financial run-qa-pairs run-flask

# Create a virtual environment
venv:
	$(PYTHON) -m venv $(VENV)

# Install dependencies
install: venv
	$(VENV)/bin/$(PIP) install -r requirements.txt

# Run the insert_financial_data.py script
run-financial:
	$(VENV)/bin/$(PYTHON) $(FINANCIAL_SCRIPT)

# Run the insert_qa_pairs.py script
run-qa-pairs:
	$(VENV)/bin/$(PYTHON) $(QA_PAIRS_SCRIPT)

# Run the Flask application
run-flask:
	$(VENV)/bin/$(FLASK) run --app app:create_app

# Run both data insertion scripts and Flask app
run: run-financial run-qa-pairs run-flask

# Run tests (if any)
test:
	$(VENV)/bin/$(PYTHON) -m unittest discover -s tests

# Clean up temporary files
clean:
	rm -rf $(VENV)
	rm -f *.log

# Lint code with pylint (including rules and main script)
lint:
	$(VENV)/bin/$(PYTHON) -m pylint $(FINANCIAL_SCRIPT) $(QA_PAIRS_SCRIPT) $(MAIN_SCRIPT) $(RULES_SCRIPT) $(RULES_DIR)*.py

# Format code with black (including rules and main script)
format:
	$(VENV)/bin/$(PYTHON) -m black $(FINANCIAL_SCRIPT) $(QA_PAIRS_SCRIPT) $(MAIN_SCRIPT) $(RULES_SCRIPT) $(RULES_DIR)*.py

# Help command to display available commands
help:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  all           - Set up environment and run both data insertion scripts and the Flask app"
	@echo "  venv          - Create a virtual environment"
	@echo "  install       - Install Python dependencies"
	@echo "  run-financial - Run the insert_financial_data.py script"
	@echo "  run-qa-pairs  - Run the insert_qa_pairs.py script"
	@echo "  run-flask     - Run the Flask app"
	@echo "  run           - Run both data insertion scripts and Flask app"
	@echo "  test          - Run unit tests"
	@echo "  clean         - Clean up temporary files"
	@echo "  lint          - Lint code with pylint"
	@echo "  format        - Format code with black"
	@echo "  help          - Display this help message"

# Phony targets
.PHONY: all venv install run-financial run-qa-pairs run-flask run test clean lint format help
