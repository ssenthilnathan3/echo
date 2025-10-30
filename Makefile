.PHONY: help install dev-install test test-unit test-integration lint format type-check clean docker-up docker-down

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	poetry install --only=main

dev-install: ## Install all dependencies including dev tools
	poetry install
	poetry run pre-commit install

test: ## Run all tests
	poetry run pytest

test-unit: ## Run unit tests only
	poetry run pytest tests/unit -v

test-integration: ## Run integration tests only
	poetry run pytest tests/integration -v

test-cov: ## Run tests with coverage
	poetry run pytest --cov=app --cov-report=html --cov-report=term

lint: ## Run linting
	poetry run ruff check .

format: ## Format code
	poetry run black .
	poetry run ruff check . --fix

type-check: ## Run type checking
	poetry run mypy .

pre-commit: ## Run all pre-commit hooks
	poetry run pre-commit run --all-files

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

docker-up: ## Start development services
	docker-compose up -d

docker-down: ## Stop development services
	docker-compose down

run-control: ## Run control plane
	poetry run uvicorn app.control_plane.main:app --reload --host 0.0.0.0 --port 8000

run-worker: ## Run worker
	poetry run python -m app.worker.main