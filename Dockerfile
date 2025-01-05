FROM python:3.10

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get -y install curl

RUN curl -sSl https://install.python-poetry.org | python3 -

RUN ~/.local/share/pypoetry/venv/bin/poetry install --no-root && ~/.local/share/pypoetry/venv/bin/poetry run invoke build

CMD ~/.local/share/pypoetry/venv/bin/poetry run invoke start
