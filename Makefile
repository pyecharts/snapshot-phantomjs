all: test

test:
	bash test.sh

format:
	isort -rc .
	black .

lint:
	make lint
