from time import sleep

import peewee as peewee
from gpiozero import CPUTemperature
import datetime

# Connect to a Postgres database. TODO: move configs out of here
pg_db = peewee.PostgresqlDatabase('postgres', user='postgres', password='raspberry',
                                  host='database', port=5432)


class BaseModel(peewee.Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pg_db

class User(BaseModel):
    username = peewee.CharField(unique=True)

class TemperatureMeasure(BaseModel):
    temperature = peewee.FloatField()
    uom = peewee.CharField()
    timestamp = peewee.DateTimeField(default=datetime.datetime.now)


def init_db():
    try:
        User.create_table()
    except peewee.OperationalError:
        print ("User table already exists!")

    try:
        TemperatureMeasure.create_table()
    except peewee.OperationalError:
        print ("CpuTemperatures table already exists!")


def start_loop():
    #just cycle over time. TODO: move configs out of here
    while(True):
        cpu = CPUTemperature()
        t=TemperatureMeasure()
        t.temperature = float(cpu.temperature)
        t.uom="°C"
        t.save()
        sleep(5)


if __name__ == '__main__':
    cpu = CPUTemperature()
    print(cpu.temperature)

    init_db()
    start_loop()




