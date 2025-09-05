.PHONY: help install install-dev run test lint format type-check clean build all

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  run          - Run the FastAPI development server"
	@echo "  run-prod     - Run the server using app settings"
	@echo "  test         - Run tests"
	@echo "  lint         - Run all linting tools (format, type-check)"
	@echo "  format       - Format code with black and isort"
	@echo "  type-check   - Run mypy type checking"
	@echo "  clean        - Clean build artifacts and cache"
	@echo "  build        - Build the package"
	@echo "  all          - Install deps, lint, test, and build"

# Install production dependencies
install:
	uv sync --no-dev

# Install development dependencies
install-dev:
	uv sync

# Run the FastAPI development server
run:
	uv run uvicorn photos_api.main:app --reload --host 0.0.0.0 --port 8000

# Run the server using main entry (uses settings)
run-prod:
	uv run python -m photos_api.main

# Run tests
test:
	uv run pytest -v

# Run tests with coverage
test-cov:
	uv run pytest --cov=photos_api --cov-report=html --cov-report=term

# Format code with black and isort
format:
	uv run black src/
	uv run isort src/

# Check code formatting (without making changes)
format-check:
	uv run black --check src/
	uv run isort --check-only src/

# Run mypy type checking
type-check:
	uv run mypy src/

# Run all linting tools
lint: format-check type-check

# Run all linting tools and fix issues where possible
lint-fix: format type-check

# Clean build artifacts and cache
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Build the package
build: clean
	uv build

# Run the complete development workflow
all: install-dev lint test build

# Development setup - run this first
setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the development server"

# Show project info
info:
	@echo "Project: photos-api"
	@echo "Python: >=3.11"
	@echo "Package Manager: uv"
	@echo "Framework: FastAPI"
	@echo ""
	@echo "Available scripts:"
	@uv run --help | grep -A 20 "Available commands:"
