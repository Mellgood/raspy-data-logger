FROM python:buster
RUN apt-get update && apt-get upgrade -y && apt-get install -y
RUN pip3 install gpiozero RPi.GPIO peewee psycopg2
WORKDIR /usr/src/app
COPY main.py .
CMD ["python", "./main.py"]