include .env
export

.PHONY: postgres
# I didn't set docker user, so I need to run docker with sudo (I'm using WSL2)
postgres:
	sudo docker start warehouse || sudo docker run --name warehouse -p 5432:5432 -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) -e POSTGRES_DB=warehouse -d postgres

.PHONY: stop-postgres
stop-postgres:
	sudo docker stop warehouse

.PHONY: drop-postgres
drop-postgres:
	sudo docker rm warehouse