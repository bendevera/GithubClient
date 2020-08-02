.PHONY: pipcompile
pipcompile:
	python3 -m piptools compile requirements.in

.PHONY: isort
isort:
	.venv/bin/isort *.py

.PHONY: venv
venv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/pip install  -r requirements.txt

.PHONY: lint
lint:
	.venv/bin/flake8 *.py

.PHONY: typecheck
typecheck:
	.venv/bin/mypy *.py

.PHONY: unit
unit:
	.venv/bin/python -m pytest -v .

.PHONY: test
test: lint typecheck unit
