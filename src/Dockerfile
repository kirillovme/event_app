FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY ./poetry.lock ./pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root --only main

COPY ./src .

RUN chmod +x entrypoint.sh
