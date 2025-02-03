CMD=go

test:
	$(CMD) test -v ./...

build:
	docker build -t kliq-collect .

run:
	docker run kliq-collect
