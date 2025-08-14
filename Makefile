# Configuration
IMAGE_NAME := github-pages-jekyll
COMMON_DOCKER_ARGS := -v $(PWD):/site -v github_pages_bundle_cache:/usr/local/bundle
COMMON_PORT := -p 4000:4000
JEKYLL_CMD := bundle exec jekyll serve --safe --livereload --host 0.0.0.0

.PHONY: build serve trace clean rebuild interactive sitemap sitemap-check validate projects

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

# Generate site map using Graphviz
sitemap: build
	@echo "Generating site map..."
	docker run --rm $(COMMON_DOCKER_ARGS) $(IMAGE_NAME) uv run python3 generate_sitemap.py --format graphviz --output assets/images/sitemap
	@echo "✅ Site map generated as assets/images/sitemap.png and assets/images/sitemap.svg"

# Validate data structures before generation
validate: build
	@echo "Validating project data..."
	docker run --rm $(COMMON_DOCKER_ARGS) $(IMAGE_NAME) bash -c "cd projects && uv run python3 validate_data.py"
	@echo "✅ Data validation completed"

# Generate projects markdown files
projects: validate
	@echo "Generating projects markdown files..."
	docker run --rm $(COMMON_DOCKER_ARGS) $(IMAGE_NAME) bash -c "cd projects && uv run python3 generate_index_md.py"
# 	@echo "Generating quarterly markdown files..."
# 	docker run --rm $(COMMON_DOCKER_ARGS) $(IMAGE_NAME) bash -c "cd projects && uv run python3 gen_quarterly_md.py"
	@echo "✅ Projects and quarterly markdown files generated"
