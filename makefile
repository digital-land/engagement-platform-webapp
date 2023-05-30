# =============================
# Utils
# =============================

server::
	python -m uvicorn application.app:app --reload --port=8080

# compile scss
scss::
	python application/core/compileSass.py './application/assets'

images::
	rm -R ./application/static/images
	cp -R ./application/assets/images ./application/static/images

javascripts::
	rm -R ./application/static/javascripts
	cp -R ./application/assets/javascripts ./application/static/javascripts

build::
	make scss
	make images
	make javascripts

# build docker image

# =============================
# Dependencies
# =============================

init::
	python -m pip install pip-tools
	make piptool-compile
	make dependencies
	make npm-dependencies
	make pre-commit-install

piptool-compile::
	python -m piptools compile --output-file=requirements/requirements.txt requirements/requirements.in
	python -m piptools compile --output-file=requirements/dev-requirements.txt requirements/dev-requirements.in

dependencies::
	pip-sync requirements/requirements.txt  requirements/dev-requirements.txt

npm-dependencies::
	npm i

pre-commit-install::
	pre-commit install

# =============================
# Linting
# =============================

lint:
	make black ./application
	python3 -m flake8 ./application
	make jslint

black-check:
	black --check .

black:
	python3 -m black .

jslint::
	npx eslint './application/**/*.js'
	npx eslint './application/**/*.html'

jslint-fix::
	npx eslint './application/**/*.js' --fix
	npx eslint './application/**/*.html' --fix

# =============================
# Testing
# =============================

test-acceptance:
	python -m playwright install chromium
	python -m pytest --md-report --md-report-color=never -p no:warnings tests/acceptance

test: test-unit test-integration

test-unit:
	python -m pytest --md-report --md-report-color=never --md-report-output=unit-tests.md tests/unit

test-integration:
	python -m pytest --md-report --md-report-color=never --md-report-output=integration-tests.md tests/integration

test-e2e:
	python -m pytest --md-report --md-report-color=never --md-report-output=e2e-tests.md tests/e2e

test-integration-docker:
	docker-compose run web python -m pytest tests/integration --junitxml=.junitxml/integration.xml $(PYTEST_RUNTIME_ARGS)

# Security
