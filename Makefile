install:
	python3 -m pip install --force-reinstall dist/*.whl
lint:
	poetry run flake8 jun_jobs_bot
pytest:
	poetry run pytest tests
test-coverage:
	poetry run pytest --cov=page_loader tests/ --cov-report xml