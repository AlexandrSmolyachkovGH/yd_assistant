FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev build-essential curl netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry config virtualenvs.create false
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root

COPY . .