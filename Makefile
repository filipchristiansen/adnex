PYTHON_VERSION = 3.10.15

.PHONY: help install_pyenv venv tests clean hooks build publish

help:
	@echo "Available Makefile targets:"
	@echo "  install_pyenv     Install pyenv and set Python version"
	@echo "  venv              Set up virtual environment with development dependencies"
	@echo "  tests             Run tests with pytest"
	@echo "  clean             Clean up project directories"
	@echo "  hooks             Run pre-commit hooks"

# Install pyenv, install python version `PYTHON_VERSION`, and set it as local version:
install_pyenv:
	brew update
	brew install pyenv
	pyenv install $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)

# Create and activate virtual environment and install necessary packages:
venv: requirements-dev.txt
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements-dev.txt
	. .venv/bin/activate && pre-commit install
	. .venv/bin/activate && pre-commit autoupdate
	make hooks

# Run pytest with coverage:
tests:
	make clean
	. .venv/bin/activate && pytest

# Clean up the project:
clean:
	find . \( -name '.DS_Store' -o -name 'Thumbs.db' \) -type f -delete
	find . -name '__pycache__' -type d -exec rm -rf {} +
	rm -rf .pytest_cache .cov .coverage src/adnex.egg-info dist/ build/

# Run pre-commit hooks:
hooks:
	. .venv/bin/activate && pre-commit run --all-files

# Build the package
build:
	python -m build

# Publish to PyPI
publish: build
	python -m twine upload dist/*
