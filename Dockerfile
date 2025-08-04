FROM python:3.11-slim-bookworm

ARG APP_VERSION=0.0.0
ARG APP_ENV="Prod"

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

COPY ai ai

COPY pyproject.toml poetry.lock README.md tasks.py start.sh pyproject.toml main.py /app/

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

RUN poetry install --without dev

RUN rm -rf ./ai/tests

# Give appuser ownership of /app
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["poetry", "run", "app", "&", "poetry", "run", "celery", "-A", "tasks", "worker", "-l", "info"]
