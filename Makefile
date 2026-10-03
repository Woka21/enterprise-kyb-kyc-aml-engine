.PHONY: up down logs build

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

api-logs:
	docker compose logs -f api

web-logs:
	docker compose logs -f web

db-logs:
	docker compose logs -f postgres
