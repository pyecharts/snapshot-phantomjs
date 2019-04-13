all: test

test:
	bash test.sh

format:
	isort -rc .
	black -l 79 .

lint:
	make lint
