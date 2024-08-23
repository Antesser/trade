start:
	python3 src/main.py
worker:
	celery -A src.tasks.tasks:celery worker --loglevel=INFO
flower:
	celery -A src.tasks.tasks:celery flower --loglevel=INFO
	