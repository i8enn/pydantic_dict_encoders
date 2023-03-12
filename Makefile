.DEFAULT_GOAL := all

# Command shortcuts
mypy = mypy pydantic_dict
ruff = ruff .
isort = isort .
black = black --fast .

# Makefile target args
args = $(filter-out $@,$(MAKECMDGOALS))

.PHONY: install
install:
	POETRY_VIRTUALENVS_IN_PROJECT=true poetry env use python3.10
	poetry install
	poetry run pip install -e .

.PHONY: build
build: clean
	poetry build

.PHONY: publish
publish:
	poetry publish

.PHONY: format
format:
	-$(isort)
	-$(black)
	-$(autopep8)

# Run linters
.PHONY: lint
lint:
	-$(isort) --check-only
	-$(black) --check
	-$(ruff)
	-$(bandit)
	-$(mypy)

.PHONY: test
test:
	pytest --no-cov-on-fail

.PHONY: testwatch
testwatch:
	pytest -fsvv --ff --color=yes ${args}

.PHONY: testcov
testcov: test
	echo "run tests and building coverage html report"
	@coverage html

.PHONY: testcov-report
testcov-report:
	echo "building coverage html report"
	@coverage html -i

.PHONY: all
all: testcov lint

.PHONY: clean
clean:
	- rm -rf `find . -name __pycache__`
	- rm -f `find . -type f -name '*.py[co]' `
	- rm -f `find . -type f -name '*~' `
	- rm -f `find . -type f -name '.*~' `
	- rm -rf .cache
	- rm -rf .*cache
	- rm -rf htmlcov
	- rm -rf *.egg-info
	- rm -f .coverage
	- rm -f .coverage.*
	- rm -rf build
	- rm -rf dist
