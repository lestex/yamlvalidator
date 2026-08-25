.PHONY: help release install-local test
.DEFAULT_GOAL := help

VERSION := $$(hatch version)

APP_NAME := yamlvalidator

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

release: ## package and upload a release
	@echo "For further usage."

install-local: ## install scaffold locally
	@echo "Make sure you activated the virtual env with: 'source .venv/bin/activate'"
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

test: ## run tests
	@pytest

coverage: ## run tests with coverage
	@pytest --cov=yamlvalidator

format: ## format python code
	@ruff format yamlvalidator tests

lint: ## run linters
	@ruff check yamlvalidator tests
	@ruff format --check yamlvalidator tests

precommit-install: ## install pre-commit
	@pre-commit install

precommit-run: ## run all pre-commit hooks
	@pre-commit run -a

clean: ## run clean up
	rm -rf .pytest_cache dist build yamlvalidator.egg-info .mypy_cache .ruff_cache .coverage
	find . -type d -name '__pycache__' -exec rm -r {} +

docker-build: ## builds docker image
	docker build -t $(APP_NAME):$(VERSION) .
