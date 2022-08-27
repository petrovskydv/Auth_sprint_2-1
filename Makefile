create-tables:
	./python3 auth_api/create_tables.py

compose:
	docker-compose -f docker-compose.yml up --build

dev-compose:
	docker-compose -f docker-compose.dev.yml up --build

superuser:
	docker exec -it auth_sprint_1_auth_api_1 bash
	python3 -m flask create-superuser EMAIL=profi@gmail.com PASSWORD=3251sdgfasg

tests:
	docker-compose exec auth_api bash
	PYTHONPATH=. pytest
