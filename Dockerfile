FROM ruby:3.1-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  nodejs \
  libffi-dev \
  zlib1g-dev \
  libssl-dev \
  python3 \
  python3-pip \
  python3-venv \
  graphviz \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /site

# Install the same version of bundler that GitHub Pages uses
RUN gem install bundler:2.4.19

# Install the github-pages gem to match GitHub's environment
COPY Gemfile Gemfile.lock* ./

# Set bundler to use system libraries when possible
RUN bundle config set force_ruby_platform true

# Install dependencies
RUN bundle install

# Rebuild eventmachine with correct OpenSSL configuration
RUN gem uninstall eventmachine --all --ignore-dependencies || true
RUN gem install eventmachine -- --with-openssl-dir=/usr

# Verify that all gems are installed
RUN bundle check

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"
RUN /root/.local/bin/uv venv
ENV VIRTUAL_ENV=/site/.venv
ENV PATH="/site/.venv/bin:$PATH"
ENV PYTHONPATH=/site/src

COPY pyproject.toml ./

RUN /root/.local/bin/uv venv
RUN /root/.local/bin/uv sync

EXPOSE 4000

# Default command that mimics GitHub Pages build process
CMD ["bundle", "exec", "jekyll", "serve", "--safe", "--livereload", "--host", "0.0.0.0"]