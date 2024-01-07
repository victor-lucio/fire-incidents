include .env
export

.PHONY: start-postgres
start-postgres:
	docker start warehouse || \
	docker run --name warehouse \
	-p 5432:5432 \
	-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	-e POSTGRES_DB=$(POSTGRES_DATABASE) \
	-d postgres

.PHONY: spin-up
spin-up:
	poetry install
	make start-postgres
	cp profiles.yml ~/.dbt/profiles.yml
	export $(cat .env | xargs)
	echo localhost:5432:warehouse:postgres:$(POSTGRES_PASSWORD) > ~/.pgpass
	chmod 0600 ~/.pgpass

.PHONY: access-postgres
access-postgres:
	psql -h localhost -U postgres -d warehouse

.PHONY: stop-postgres
stop-postgres:
	docker stop warehouse

.PHONY: drop-postgres
drop-postgres:
	docker stop warehouse
	docker rm warehouse

.PHONY: format
format:
	ruff format .

.PHONY: check-format
check-format:
	ruff check .

.PHONY: run-load-fire-incidents-raw
run-load-fire-incidents-raw:
	poetry python fire_incidents/jobs/load_fire_incidents_raw.py $(RUN_DATE)

.PHONY: run-dbt-models
run-dbt-models:
	cd dbt && poetry run dbt run