.DEFAULT_GOAL := help
help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

format: ## Format style with black
	black --exclude="/(postgres_data|venv|migrations|\.git)/" core/ apps/ scripts/ tests/

test: ## Tests
	docker-compose -f docker-compose.dev.yaml exec -T django bash -c "pytest"

docker.recreate.django: ## Recreate Django image
	docker-compose -f docker-compose.dev.yaml build --no-cache --force-rm django
	docker-compose -f docker-compose.dev.yaml up --force-recreate --no-deps -d django
	## make run.loaddata

run.makemigrations: ## Makemigrations
	docker-compose -f docker-compose.yaml exec -T django bash -c "python3 manage.py makemigrations"

run.migrate: ## Migrate
	docker-compose -f docker-compose.yaml exec -T django bash -c "python3 manage.py migrate"

run.loaddata: ## Load initial data
	# Remove database
	docker-compose exec -T django bash -c "python3 manage.py flush --noinput"
	# Remove media
	rm -rf media
	# Migrate
	docker-compose exec -T django bash -c "python3 manage.py migrate"

run.loaddata.fake: ## Load initial data test
	make run.loaddata
	# Add superuser: alias "admin" - password "admin"
	docker-compose -f docker-compose.dev.yaml exec -T django bash -c "cat data/create_superuser.py | python3 manage.py shell"

run.server.dev: ## Run server
	docker-compose -f docker-compose.dev.yaml up

run.server.pro: ## Run server
	docker-compose -f docker-compose.pro.yaml up
