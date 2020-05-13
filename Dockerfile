FROM python:3.6-alpine as builder

LABEL maintainer="carl.wilson@openpreservation.org" \
      org.openpreservation.vendor="Open Preservation Foundation" \
      version="0.1"

RUN  apk update && apk --no-cache --update-cache add gcc build-base libxml2-dev libxslt-dev git

WORKDIR /src

COPY setup.py setup.py
COPY requirements.txt requirements.txt
COPY README.md README.md
COPY ip_validation/* ip_validation/

RUN mkdir /install && pip install -U pip && pip install -r requirements.txt --prefix=/install && pip install git+https://github.com/E-ARK-Software/eatb.git@refact/tests_and_resources --prefix=/install && pip install --prefix=/install .

FROM python:3.6-alpine

RUN apk update && apk add --no-cache --update-cache libc6-compat libstdc++ bash libxslt
RUN install -d -o root -g root -m 755 /opt && adduser --uid 1000 -h /opt/ip_validation -S eark && pip install -U pip python-dateutil

WORKDIR /opt/ip_validation

COPY --from=builder /install /usr/local
COPY . /opt/ip_validation/
RUN chown -R eark:users /opt/ip_validation

USER eark

EXPOSE 5000
ENV FLASK_APP='ip_validation'
ENTRYPOINT flask run --host "0.0.0.0" --port "5000"
