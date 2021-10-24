PROJECT_NAME ?= cicdschool21
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= kudddy
REGISTRY_IMAGE ?= docker.io/$(PROJECT_NAMESPACE)/$(PROJECT_NAME)

all:
	@echo "make devenv		- Создать и установить тестововой окружение"
	@echo "make lint		- Проверить код с помощью pylint"
	@echo "make postgres	- Запустить контейнер с postgres"
	@echo "make test		- запустить тесты"
	@echo "make docker		- Build a docker image"
	@echo "make upload		- Upload docker image to the registry"
	@exit 0

clean:
	rm -fr *.egg-info dist

devenv: clean
	rm -rf env
	# создаем новое окружение
	python3.8 -m venv env
	# обновляем pip
	env/bin/pip install -U pip

lint:
	env/bin/pylama

postgres:
	docker run -d --rm --name some-postgres -p 5434:5432 \
		-e POSTGRES_PASSWORD=pass -e POSTGRES_USER=user -e \
		POSTGRES_DB=db postgres:9.6


test: lint postgres
	env/bin/pytest -vv --cov=analyzer --cov-report=term-missing tests

docker:
	docker build -t $(REGISTRY_IMAGE) .

upload: docker
	docker push $(REGISTRY_IMAGE):latest
