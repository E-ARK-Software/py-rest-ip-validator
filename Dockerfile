FROM python:3.9-alpine

LABEL maintainer="carl.wilson@openpreservation.org" \
      org.openpreservation.vendor="Open Preservation Foundation" \
      version="0.1"

RUN  apk update && apk --no-cache --update-cache add gcc build-base libxml2-dev libxslt-dev openjdk11

RUN mkdir -p /usr/src/eark_ip
WORKDIR /usr/src/eark_ip
COPY ./eark_ip_valid/ /usr/src/eark_ip/
RUN pip3 install --no-cache-dir .

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./eark_ip_rest/ /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir .
COPY ./eark_ip_valid/eark_ip/api/resources/schemas/*.xsd /usr/local/lib/python3.9/site-packages/eark_ip/api/resources/schemas/
COPY ./eark_ip_valid/eark_ip/api/resources/profiles/*.xml /usr/local/lib/python3.9/site-packages/eark_ip/api/resources/profiles/
COPY ./eark_ip_valid/eark_ip/api/resources/schematron/*.xml /usr/local/lib/python3.9/site-packages/eark_ip/api/resources/schematron/
COPY ./eark_ip_rest/eark_ip_rest/resources/commons-ip2-cli-2.0.1.jar /usr/local/lib/python3.9/site-packages/eark_ip_rest/resources/commons-ip2-cli-2.0.1.jar
RUN pip3 freeze
RUN pwd
RUN ls -alh
EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "eark_ip_rest"]
