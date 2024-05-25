# Dockerfile for netprobe_lite
FROM python:3.12-slim-bookworm as builder

ENV \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN pip3 install --no-cache-dir poetry==1.8.3

COPY . ./

RUN poetry install --only main -vv

FROM python:3.12-slim-bookworm as runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" 

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping=3:20221126-1 \
    traceroute=1:2.1.2-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app /app


