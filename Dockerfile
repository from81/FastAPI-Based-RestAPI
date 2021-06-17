FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set up project directory
COPY ./app /app
COPY ./requirements.txt /requirements.txt
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get upgrade -yqq 
RUN pip install --user -r /requirements.txt
RUN apt-get clean
