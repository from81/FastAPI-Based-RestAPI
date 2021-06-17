FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set up project directory
COPY ./app /app
COPY ./requirements.txt /requirements.txt

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && pip install --user -r /requirements.txt \
    && apt-get clean

