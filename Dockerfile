# Dockerfile for netprobe_lite
# https://github.com/plaintextpackets/netprobe_lite/
FROM python:3.12-slim-bookworm as builder

ENV \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN pip3 install poetry

COPY . ./

RUN poetry install --only main -vv

FROM python:3.12-slim-bookworm as runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" 

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
    iputils-ping \
    traceroute \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app /app


