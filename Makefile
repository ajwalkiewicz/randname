.PHONY: setup check-uv build test test_all \
	clean clean_venv clean_build clean_cache \
	format check lint type docs docs_upload docs_build \
	coverage

setup: check-uv uv.lock
	@echo "Setting up project..."
	uv sync

	
check-uv:
	@if ! command -v uv > /dev/null; then \
		echo "UV is not installed"; \
		echo "Installing UV"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

build: check test clean_build
	@echo "Building package..."
	uv build

test: tests/test_*.py
	@echo "Running tests..."
	@if ! uv run pytest -m "not slow"; then \
		echo "Tests failed. Building project not possible."; \
		exit 1; \
	fi

test_all: tests/test_*.py
	@echo "Running all tests..."
	@if ! uv run pytest; then \
		echo "Tests failed. Building project not possible."; \
		exit 1; \
	fi

clean: clean_venv clean_build clean_cache

clean_venv:
	@echo "Removing virtual environment.."
	rm -rf .venv

clean_build:
	@echo "Removing build files..."
	rm -rf dist/

clean_cache:
	@echo "Removing all cache files and directories int the project..." 
	find . -name "*cache*" -type d | xargs -t -I {} rm -rf "{}"

format:
	@echo "Formatting project files with ruff..."
	uv run ruff format src/ tests/

check: lint type

lint:
	@echo "Linting project files with ruff..."
	uv run ruff check src/ tests/

type:
	@echo "checking typing with mypy..."
	uv run mypy src/ tests/

docs: docs
	uv run mkdocs serve

docs_upload:
	uv run mkdocs gh-deploy

docs_build:
	uv run mkdocs build

coverage: 
	@echo "Generating test coverage report..."
	uv run pytest --cov=randname --cov-report=term-missing --cov-report=html