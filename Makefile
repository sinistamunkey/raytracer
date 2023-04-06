.PHONY: all
all: lint test

format:
	@echo "Formatting"
	isort --profile black .
	black .

lint:
	@echo "Linting"
	flake8 .
	mypy raytracer
	black --check --diff .

test:
	@echo "Testing"
	pytest -x --cov=tests --cov=raytracer
