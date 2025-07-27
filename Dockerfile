FROM python:3.11.9-slim

WORKDIR /app

COPY ai ai

RUN pip install poetry

COPY pyproject.toml  poetry.lock README.md tasks.py ./

RUN poetry install

CMD ["poetry", "run", "app"]
