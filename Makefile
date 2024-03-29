lint:
	poetry run flake8 jun_jobs_bot
	poetry run black . --check

test:
	poetry run pytest tests

test-coverage:
	poetry run pytest --cov=jun_jobs_bot tests/ --cov-report xml

run:
	poetry run bot

p_install:
	poetry install
	poetry build

install:
	pip install -r requirements.txt
