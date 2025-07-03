.PHONY: run test lint build docker-up docker-down

run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests

lint:
	flake8 src tests

build:
	docker build -t ticketing-api .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
