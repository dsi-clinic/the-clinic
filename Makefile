# This is used for building and previewing locally

.PHONY: build serve clean

build:
	docker build -t jekyll-site .

serve: build
	docker run --rm -v ${PWD}:/site -p 4000:4000 \
        jekyll-site bundle exec jekyll serve --host 0.0.0.0 --livereload

interactive: build
	docker run --rm -it -v ${PWD}:/site -p 4000:4000 \
        jekyll-site /bin/bash

clean:
	docker rmi jekyll-site