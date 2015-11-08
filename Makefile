all: build

lint:
	@python cinspector.py lint

validate:
	@python cinspector.py validate

build: lint validate
	@echo "docker build"
