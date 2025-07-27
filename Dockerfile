FROM python:3.11-slim-bookworm

WORKDIR /app

COPY ai ai

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md tasks.py ./

RUN poetry install --without dev

CMD ["poetry", "run", "app"]
