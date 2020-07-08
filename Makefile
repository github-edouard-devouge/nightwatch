NAME ?= $(shell basename $(PWD))
VERSION := $(shell cat .VERSION)
HASH :=  $(shell git rev-parse --short HEAD)

PY_SOURCE_PATH := ./src
PY_DIST_PATH := ./dist

JS_SOURCE_PATH := ./webui/nightwatch
JS_DIST_PATH := $(JS_SOURCE_PATH)/dist

REGISTRY ?= "${DEFAULT_REGISTRY}"
AWS_REGION ?= eu-west-1
CUSTOM_BUILD_ARGS = --build-arg projectName=$(NAME)
DOCKER_ROOT := ./


K8S_NAMESPACE ?= default
K8S_RESOURCE_KIND ?= deployment
K8S_RESOURCE_NAME ?= $(NAME)
K8S_CONTAINER_NAME ?= $(NAME)

all: build-docker tag ecr-login push clean

.PHONY: init
init:
	./.init/init.sh $(NAME)

.PHONY: build
build: clean auto-increment-version build-docker

.PHONY: build-nc
build-nc: clean auto-increment-version build-docker-nc

.PHONY: build-js
build-js:
	npm run build --prefix $(JS_SOURCE_PATH)

.PHONY: build-py
build-py:
	python3 setup.py sdist bdist_wheel --dist-dir $(PY_DIST_PATH)

.PHONY: build-docker
build-docker:
	docker build $(CUSTOM_BUILD_ARGS) -t $(NAME):$(VERSION)-$(HASH) $(DOCKER_ROOT)

.PHONY: build-docker-nc
build-docker-nc:
	docker build $(CUSTOM_BUILD_ARGS) --no-cache -t $(NAME):$(VERSION)-$(HASH) $(DOCKER_ROOT)

.PHONY: auto-increment-version
auto-increment-version:
	$(shell source .init/increment-version.sh && increment_version $(VERSION) > .VERSION)
	$(eval VERSION=$(shell cat .VERSION))

.PHONY: release-minor-version
release-minor-version:
	$(shell source .init/increment-version.sh && increment_version $(VERSION) 2 > .VERSION)
	$(eval VERSION=$(shell cat .VERSION))
	$(shell git tag -a v$(VERSION) -m "Release of minor version $(VERSION)")
	@echo "Release of minor version $(VERSION)"

.PHONY: release-major-version
release-major-version:
	$(shell source .init/increment-version.sh && increment_version $(VERSION) 1 > .VERSION)
	$(eval VERSION=$(shell cat .VERSION))
	$(shell git tag -a v$(VERSION) -m "Release of major version $(VERSION)")
	@echo "Release of major version $(VERSION)"

.PHONY: tag
tag:
	docker tag $(NAME):$(VERSION)-$(HASH) $(REGISTRY)/$(NAME):$(VERSION)-$(HASH)
	docker tag $(NAME):$(VERSION)-$(HASH) $(NAME):latest
	docker tag $(NAME):$(VERSION)-$(HASH) $(REGISTRY)/$(NAME):latest

.PHONY: ecr-login
ecr-login:
	aws ecr get-login --no-include-email --region $(AWS_REGION) | /bin/bash

.PHONY: push
push:
	docker push $(REGISTRY)/$(NAME):$(VERSION)-$(HASH)
	docker push $(REGISTRY)/$(NAME):latest

.PHONY: clean
clean:
	rm -rf $(PY_DIST_PATH)
	rm -rf $(JS_DIST_PATH)

.PHONY: deploy-to-k8s
deploy-to-k8s:
	kubectl set image -n $(K8S_NAMESPACE) $(K8S_RESOURCE_KIND)/$(K8S_RESOURCE_NAME) $(K8S_CONTAINER_NAME)=$(REGISTRY)/$(NAME):$(VERSION)-$(HASH)
