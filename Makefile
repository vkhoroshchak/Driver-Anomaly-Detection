.PHONY: build start stop

build: Dockerfile pyproject.toml
	docker build --no-cache -f Dockerfile .

start:
	docker-compose up -d

stop:
	docker-compose down

#* Ruff (linting&formatting)
.PHONY: check-codestyle codestyle formatting
check-codestyle:
	poetry run ruff check .

codestyle:
	poetry run ruff check . --fix

formatting:
	poetry run ruff format .

#* Cleaning
.PHONY: pycache-remove dsstore-remove pytestcache-remove ruff-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

ruff-remove:
	find . | grep -E ".ruff_cache" | xargs rm -rf