FROM --platform=linux/amd64 python:3.11-buster
WORKDIR /tmp
RUN apt update
RUN apt install -y python3-pip python3-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
ARG REPOPATH
COPY scripts .
CMD ["/tmp/eval-repo.sh"]