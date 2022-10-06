create-tables:
	./python3 auth_api/create_tables.py

compose:
	docker-compose -f docker-compose.yml up --build

dev-compose:
	docker-compose -f docker-compose.dev.yml up --build

