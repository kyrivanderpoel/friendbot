FROM python:3.8-alpine
RUN mkdir /usr/src/app
RUN apk update \
    && apk add \
    gcc \
    linux-headers \
    libc-dev \
    curl
WORKDIR /usr/src/app
COPY . .
RUN pip install --editable .
