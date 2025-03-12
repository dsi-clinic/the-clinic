# Configuration
IMAGE_NAME := github-pages-jekyll
COMMON_DOCKER_ARGS := -v $(PWD):/site -v github_pages_bundle_cache:/usr/local/bundle
COMMON_PORT := -p 4000:4000
JEKYLL_CMD := bundle exec jekyll serve --safe --livereload --host 0.0.0.0

.PHONY: build serve trace clean rebuild interactive

# Build the Docker image
build: 
	docker build . -t $(IMAGE_NAME)

# Run with GitHub Pages compatibility settings
serve: build
	docker run $(COMMON_DOCKER_ARGS) $(COMMON_PORT) $(IMAGE_NAME) $(JEKYLL_CMD)

# Enter interactive shell in the container
interactive: build
	docker run -it $(COMMON_DOCKER_ARGS) $(IMAGE_NAME) /bin/bash

# Run server with trace option for debugging
trace: build
	docker run $(COMMON_DOCKER_ARGS) $(COMMON_PORT) $(IMAGE_NAME) $(JEKYLL_CMD) --trace

# Clean up Docker resources
clean:
	-docker stop $$(docker ps -a --filter volume=github_pages_bundle_cache -q)
	-docker rm $$(docker ps -a --filter volume=github_pages_bundle_cache -q)
	-docker volume rm github_pages_bundle_cache

# Complete rebuild and serve
rebuild: clean build serve
	@echo "Rebuild complete"

# For GitHub Pages emulation - check what plugins/features are available
plugins:
	docker run --rm $(COMMON_DOCKER_ARGS) $(IMAGE_NAME) bundle exec github-pages versions
