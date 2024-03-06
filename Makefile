build:
	docker-compose build

up:
	docker-compose up -d

up-attached:
	docker-compose up

down:
	docker-compose down

flake8:
	docker-compose run --rm backend sh -c "flake8"

flake8-with-backend-running:
	docker-compose exec backend flake8 .

start-project:
	docker-compose run --rm backend sh -c "django-admin startproject app ." 

