#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
FROM python:3.7

RUN pip install pipenv
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pipenv install -d --system

WORKDIR /app

CMD ["pipenv", "run", "webserver"]
