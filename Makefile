install:
	poetry install
	poetry build
	python3 -m pip install --user --force-reinstall dist/*.whl

install-venv:
	poetry install
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 jun_jobs_bot
pyt:
	poetry run pytest tests
test-coverage:
	poetry run pytest --cov=page_loader tests/ --cov-report xml