# syntax=docker/dockerfile:1

FROM python:3.12.2-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    \
    apt update && \
    apt install -y make && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* \
    && \
    adduser \
        --disabled-password \
        --gecos "" \
        --home "/nonexistent" \
        --shell "/sbin/nologin" \
        --no-create-home \
        --uid "10001" \
        appuser \
    && \
    python -m pip install -r requirements.txt

USER appuser

COPY . .

EXPOSE 8000

CMD make start
