# This is used, in conjunction with the makefile
# for previewing changes locally
FROM ruby:3.2-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /site

COPY Gemfile .
RUN bundle install

EXPOSE 4000