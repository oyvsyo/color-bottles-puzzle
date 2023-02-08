PACKAGE := color_bottles

# MAIN TASKS ##################################################################

.PHONY: all
all: install

.PHONY: ci
ci: format check tests-coverage  ## Run all tasks that determine CI status

# PROJECT DEPENDENCIES ########################################################

.PHONY: install
install:  ## Install deps and tha package
	@ poetry install -q

.PHONY: format
format: install  # Run formatters: black, isort
	poetry run isort $(PACKAGE) tests
	poetry run black $(PACKAGE) tests

.PHONY: check
check: install format  ## Run formatters, linters, and static analysis
	poetry run mypy $(PACKAGE) tests
	poetry run pylint $(PACKAGE) tests
	poetry run pydocstyle $(PACKAGE) tests

.PHONY: tests
tests: install  ## Run tests
	poetry run pytest tests

.PHONY: tests-coverage
tests-coverage: install  ## Run tests with coverage
	poetry run pytest tests \
		--verbose \
		--junit-xml=.cache/coverage/report.xml \
		--cov-report html \
		--cov-report xml \
		--cov-report term \
		--cov=$(PACKAGE) \
		--cov=tests \
		$(testsdir)

# BUILD #######################################################################

.PHONY: dist
dist: install  ## Build dist to be ready to publish
	poetry build

# CLEAN #####################################################################

.PHONY: clean
clean:  ## Remove caches and dist folders
	rm -rf .cache dist */*__pycache__* */*/*__pycache__*

# HELP #####################################################################
.DEFAULT_GOAL := help
help: Makefile ## Prints this help to stdout
	@ echo "Available tasks to do:"
	@ grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | \
 	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | \
 	sed -e 's/\[32m##/[33m/'
