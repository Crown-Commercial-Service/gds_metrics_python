.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Run tests
	flake8
	python setup.py test

.PHONY: build-wheel
build-wheel: ## build distributable wheel
	pip install wheel
	python setup.py bdist_wheel

.PHONY: publish-to-pypi
publish-to-pypi: build-wheel ## upload distributable wheel to pypi
	pip install --upgrade twine
	@twine upload dist/*.whl \
		--repository-url=https://upload.pypi.org/legacy/ \
		--username="${PYPI_USERNAME}" \
		--password="${PYPI_PASSWORD}" \
		--skip-existing # if you haven't run `make clean` there may be old wheels - don't try and re-upload them

.PHONY: clean
clean: ## clean cache, venv, dist eggs
	rm -rf .cache venv dist .eggs build
