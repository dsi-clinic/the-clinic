FROM ruby:3.1-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  nodejs \
  libffi-dev \
  zlib1g-dev \
  libssl-dev

WORKDIR /site

# Install the same version of bundler that GitHub Pages uses
RUN gem install bundler:2.4.19

# Install the github-pages gem to match GitHub's environment
COPY Gemfile Gemfile.lock* ./

# Set bundler to use system libraries when possible
RUN bundle config set force_ruby_platform true

# Install dependencies
RUN bundle install

# Verify that all gems are installed
RUN bundle check

EXPOSE 4000

# Default command that mimics GitHub Pages build process
CMD ["bundle", "exec", "jekyll", "serve", "--safe", "--livereload", "--host", "0.0.0.0"]