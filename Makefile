.PHONY: help

clean: ## Clean environment
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f *.log

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check:  ## Run static code checks
	@flake8 .
	@isort --check
	@black --check .

fix-code:  ## Fix some code style
	@isort -rc .
	@black .

test:  ## Run unit tests
	@py.test -x tests/

coverage: ## Run unit tests coverage
	@py.test -x --cov ramos/ --cov-report=xml --cov-report=term-missing tests/

outdated: ## Show outdated dependencies
	@pip list --outdated --format=columns

install:  ## Install development dependencies
	@pip install -r requirements-dev.txt

release-draft: ## Show new release changelog
	@towncrier --draft

release-patch: ## Create patch release
	@bumpversion patch --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	@git commit -am 'Update CHANGELOG'
	@bumpversion patch

release-minor: ## Create minor release
	@bumpversion minor --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	@git commit -am 'Update CHANGELOG'
	@bumpversion minor

release-major: ## Create major release
	@bumpversion major --dry-run --no-tag --no-commit --list | grep new_version= | sed -e 's/new_version=//' | xargs -n 1 towncrier --yes --version
	@git commit -am 'Update CHANGELOG'
	@bumpversion major
