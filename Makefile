compose-up:
	docker-compose -f docker-compose.yml up --build -d
compose-down:
	docker-compose -f docker-compose.yml down -v

rebuilt-etl:
	docker-compose up -d --no-deps --build etl-postgres-elastic
rebuilt-admin:
	docker-compose up -d --no-deps --build movies-admin-panel

migrate-admin-fake:
	docker-compose exec movies-admin-panel python manage.py migrate movies --fake
migrate-admin:
	docker-compose exec movies-admin-panel python manage.py migrate
collectstatic-admin:
	docker-compose exec movies-admin-panel python manage.py collectstatic
make_superuser-admin:
	docker-compose exec movies-admin-panel python manage.py createsuperuser --noinput --username 'test' --email 'test@test.com'

clean-pyenv:
	pip freeze | xargs pip uninstall -y
