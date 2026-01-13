.PHONY: help install install-dev run init-db clean test lint format backup

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make run          - Run the application"
	@echo "  make init-db      - Initialize the database"
	@echo "  make clean        - Clean up temporary files"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linter"
	@echo "  make format       - Format code"
	@echo "  make backup       - Backup database"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	python run.py

init-db:
	flask init-db

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf build dist .pytest_cache .coverage htmlcov

test:
	pytest

lint:
	flake8 app
	pylint app

format:
	black app

backup:
	@echo "Creating backup..."
	@mkdir -p backups
	@cp erp_system.db backups/erp_system_$(shell date +%Y%m%d_%H%M%S).db
	@echo "Backup created successfully!"

