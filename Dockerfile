FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY apache_exporter /usr/src/app/apache_exporter

EXPOSE 8000

ENTRYPOINT [ "python", "-m", "apache_exporter" ]
