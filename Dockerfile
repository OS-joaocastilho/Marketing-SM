FROM python:3.12.4-slim

## Install OS dependencies
RUN pip install --upgrade pip
RUN pip install poetry==1.7

WORKDIR /

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY README.md README.md
COPY data data
COPY app app
COPY marketing_sm marketing_sm

RUN poetry install

CMD ["poetry", "run", "python", "-m", "marketing_sm.app"]
