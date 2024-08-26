start:
	python3 src/main.py
worker:
	celery -A tasks.tasks:celery worker --loglevel=INFO
flower:
	celery -A tasks.tasks:celery flower --loglevel=INFO
redis:
	redis-cli	