FROM python:3.13.1-slim

# set workdir
WORKDIR /app

RUN apt update && \
    apt upgrade -y && \
    apt install -y libpq-dev build-essential make && \
    pip install --upgrade pip poetry

# install requirements
COPY ./db/poetry.lock ./db/pyproject.toml ./db/Makefile /app/
RUN poetry config virtualenvs.create false
RUN make poetry:install

CMD ["/bin/bash", "-c", "alembic upgrade head"]