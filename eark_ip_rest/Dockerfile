FROM python:3.6-alpine

LABEL maintainer="carl.wilson@openpreservation.org" \
      org.openpreservation.vendor="Open Preservation Foundation" \
      version="0.1"

RUN  apk update && apk --no-cache --update-cache add gcc build-base libxml2-dev libxslt-dev

RUN mkdir -p /usr/src/eark_ip
WORKDIR /usr/src/eark_ip
COPY ./eark_ip_valid/* /usr/src/eark_ip/
RUN pip3 install --no-cache-dir .

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./eark_ip_server/* /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 freeze
RUN pwd
RUN ls -alh
EXPOSE 8080

ENTRYPOINT ["eark_ip_rest"]
