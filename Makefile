compose-up:
	docker-compose -f docker-compose.yml up --build -d
compose-down:
	docker-compose -f docker-compose.yml down -v
rebuilt-etl:
	docker-compose up -d --no-deps --build etl-postgres-elastic
clean-pyenv:
	pip freeze | xargs pip uninstall -y
