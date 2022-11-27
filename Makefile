install:
	poetry install
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 jun_jobs_bot

test:
	poetry run pytest tests

test-coverage:
	poetry run pytest --cov=jun_jobs_bot tests/ --cov-report xml