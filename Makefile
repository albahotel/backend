default: build run;

build:
	docker compose build

run:
	docker compose up

format:
	ruff format .