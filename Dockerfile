FROM python:3.11-slim-bookworm

ARG APP_VERSION=0.0.0
ARG APP_ENV="Prod"

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

COPY ai ai

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md tasks.py start.sh ./

RUN poetry install --without dev

RUN rm -rf ./ai/tests

USER appuser

CMD ["./start.sh"]
