#####################################################################
### DEPENDENCIES INSTALLATION
#####################################################################
FROM python:3.11.8-bullseye AS build-stage

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# RUN apt-get update apt-get -y install libpq-dev gcc

RUN apt-get update && apt-get install -y build-essential cmake

RUN pip install --upgrade pip
RUN pip install --upgrade wheel

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN pip uninstall wheel -y
RUN pip uninstall pip -y

WORKDIR /opt/venv
RUN find . -name *.pyc -delete

################################################
FROM python:3.11.8-bullseye AS deploy-stage
LABEL maintainer="sergio.mora@scmlatam.com"

COPY --from=build-stage /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./src/ /opt/src
WORKDIR /opt/

EXPOSE ${PORT}
ENV PYTHONUNBUFFERED 1
ENV SQLALCHEMY_WARN_20 1

CMD uvicorn src.main:app --host=0.0.0.0 --port=${PORT}