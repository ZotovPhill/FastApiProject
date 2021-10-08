app_name?=backend-fapi
root_path?=app
config_path?=app/orm/fixtures/config/fixtures_v1.yaml
message?=migration message
with_data?=false
version?=head
environment?=dev

migration:
	docker exec -it $(app_name) sh -c "alembic  revision --autogenerate -m \"$(message)\""

migrate:
	docker exec -it $(app_name) sh -c "alembic  -x data=$(with_data) upgrade $(version)"

downgrade:
	docker exec -it $(app_name) sh -c "alembic  downgrade $(version)"

load-fixtures:
	docker exec -it $(app_name) sh -c "python -m $(root_path).commands.fixtures create-config $(config_path) -e $(environment) -s"

truncate_database:
	docker exec -it $(app_name) sh -c "python -m $(root_path).commands.fixtures truncate-db"

pytest:
	docker exec -it $(app_name) sh -c "pytest $(root_path)"

coverage:
	docker exec -it $(app_name) sh -c "coverage run -m pytest $(root_path) && coverage report -m"

flake8:
	docker exec -it $(app_name) sh -c "flake8"

mypy:
	docker exec -it $(app_name) sh -c "mypy . --ignore-missing-imports"

nox:
	docker exec -it $(app_name) sh -c "nox"

black:
	docker exec -it $(app_name) sh -c "black --check . -v"