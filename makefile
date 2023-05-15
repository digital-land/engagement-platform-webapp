init::
	python -m pip install pip-tools
	make dependencies
	make piptool-compile

piptool-compile::
	python -m piptools compile --output-file=requirements/requirements.txt requirements/requirements.in

dependencies::
	pip-sync requirements/requirements.txt

server::
	python -m uvicorn application.app:app --reload --port=8080

# Testing
# Security