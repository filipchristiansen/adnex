PYTHON_VERSION = 3.10.15

# Install pyenv, install python version `PYTHON_VERSION`, and set it as local version:
.PHONY: install_pyenv
install_pyenv:
	brew update
	brew install pyenv
	pyenv install $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)

# Create and activate virtual environment and install necessary packages:
.PHONY: venv
venv: requirements.txt
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	. .venv/bin/activate && pre-commit install
	. .venv/bin/activate && pre-commit autoupdate
	make hooks

# Run pytest with coverage:
.PHONY: tests
tests:
	make clean
	. .venv/bin/activate && pytest

# Clean up the project:
.PHONY: clean
clean:
	find . \( -name '.DS_Store' -o -name 'Thumbs.db' \) -type f -delete
	find . -name '__pycache__' -type d -exec rm -rf {} +
	rm -rf .pytest_cache .cov .coverage

# Run pre-commit hooks:
.PHONY: hooks
hooks:
	. .venv/bin/activate && pre-commit run --all-files
