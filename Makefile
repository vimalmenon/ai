.PHONY: test test-fast test-cov test-unit test-integration test-units test-apis test-parallel test-file test-pattern test-watch pre-push quality-check help clean lint format setup

# Python executable path
PYTHON := .tox/py313/bin/python

# Default target
help:
	@echo "Available commands:"
	@echo "  test          - Run all tests"
	@echo "  test-fast     - Run tests with fast mode (stop on first failure)"
	@echo "  test-cov      - Run tests with coverage report"
	@echo "  test-unit     - Run only unit tests (with markers or fallback)"
	@echo "  test-integration - Run only integration tests (with markers or fallback)"
	@echo "  test-units    - Run manager and service tests"
	@echo "  test-apis     - Run API tests"
	@echo "  test-parallel - Run tests in parallel"
	@echo "  test-watch    - Run tests in watch mode"
	@echo "  test-file FILE=<path> - Run specific test file"
	@echo "  test-pattern PATTERN=<name> - Run tests matching pattern"
	@echo "  pre-push      - Run all quality checks before pushing"
	@echo "  quality-check - Alias for pre-push"
	@echo "  clean         - Clean test artifacts"
	@echo "  lint          - Run linting tools"
	@echo "  format        - Format code"

# Run all tests
test:
	$(PYTHON) -m pytest

# Run tests in fast mode (stop on first failure)
test-fast:
	$(PYTHON) -m pytest -x --tb=line

# Run tests with coverage
test-cov:
	$(PYTHON) -m pytest --cov=ai --cov-report=term-missing --cov-report=html

# Run only unit tests
test-unit:
	$(PYTHON) -m pytest -m "unit" || $(PYTHON) -m pytest ai/tests/managers/ ai/tests/services/ --tb=short

# Run only integration tests  
test-integration:
	$(PYTHON) -m pytest -m "integration" || $(PYTHON) -m pytest ai/tests/api/ --tb=short

# Run tests in parallel
test-parallel:
	$(PYTHON) -m pytest -n auto

# Run tests in watch mode
test-watch:
	poetry run pytest-watch --config pytest.ini

# Run tests without markers (managers and services)
test-units:
	$(PYTHON) -m pytest ai/tests/managers/ ai/tests/services/ --tb=short

# Run tests without markers (api tests)
test-apis:
	$(PYTHON) -m pytest ai/tests/api/ --tb=short

# Clean test artifacts
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Run linting tools
lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy ai/
	$(PYTHON) -m flake8 ai/

# Format code
format:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .
	$(PYTHON) -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place .

# Development setup
setup:
	poetry install
	poetry run tox -e py313

# Run specific test file
test-file:
	@if [ -z "$(FILE)" ]; then echo "Usage: make test-file FILE=path/to/test_file.py"; exit 1; fi
	$(PYTHON) -m pytest $(FILE) -v

# Run tests matching a pattern
test-pattern:
	@if [ -z "$(PATTERN)" ]; then echo "Usage: make test-pattern PATTERN=test_name_pattern"; exit 1; fi
	$(PYTHON) -m pytest -k "$(PATTERN)" -v

# Pre-push checks - run all quality checks before pushing
pre-push:
	@echo "🚀 Running pre-push checks..."
	@echo "📋 Running linting checks..."
	$(PYTHON) -m black --check --diff .
	$(PYTHON) -m ruff check .
	$(PYTHON) -m flake8 .
	@echo "🔍 Running type checking..."
	$(PYTHON) -m mypy ai/
	@echo "🧪 Running tests..."
	$(PYTHON) -m pytest -n auto --cov=ai --cov-report=term-missing -q
	@echo "✅ All pre-push checks passed!"

# Full quality check (alias for pre-push)
quality-check: pre-push
