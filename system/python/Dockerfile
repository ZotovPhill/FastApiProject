FROM python:3.9.6-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get -y update \
    && apt-get -y install git \
    && apt-get clean

RUN python -m pip install -U pip
RUN pip install poetry

WORKDIR /usr/src/fapi

ENV PATH /fastapiproject/.venv/bin:$PATH
ENV PYTHONPATH "${PYTHONPATH}:/fastapiproject/.venv/bin"

ARG SYSTEM_PATH=system/python
COPY ["${SYSTEM_PATH}/*", "./"]
RUN poetry config virtualenvs.create false \
  && poetry install -E apgsql

COPY app app
RUN chmod +x entrypoint.sh entrypoint-celery.sh
