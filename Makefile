all: build

lint:
	@dli lint

validate:
	@dli validate

build: lint validate
	@echo "docker build"
