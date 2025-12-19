IMAGE_NAME ?= wishlist-api
TAG ?= latest

.PHONY: docker-build docker-run docker-down docker-scan lint

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

docker-run:
	docker compose up --build

docker-down:
	docker compose down

docker-scan:
	@echo "Running Trivy scan (requires docker & trivy)..."
	trivy image --exit-code 0 --severity HIGH,CRITICAL $(IMAGE_NAME):$(TAG)

lint:
	@echo "Run hadolint (requires hadolint)..."
	hadolint Dockerfile
