from time import sleep

import peewee as peewee
from gpiozero import CPUTemperature
import datetime

# Connect to a Postgres database.
pg_db = peewee.PostgresqlDatabase('postgres', user='postgres', password='pipponde',
                                  host='database', port=5432)

def testdb():
    try:
        User.create_table()
    except peewee.OperationalError:
        print ("User table already exists!")

    try:
        TemperatureMeasure.create_table()
    except peewee.OperationalError:
        print ("CpuTemperatures table already exists!")

    a = User()
    a.username = "carlo"
    a.save(force_insert=True)



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


if __name__ == '__main__':
    cpu = CPUTemperature()
    print(cpu.temperature)

    init_db()

    while(True):
        cpu = CPUTemperature()
        t=TemperatureMeasure()
        t.temperature = float(cpu.temperature)
        t.uom="°C"
        t.save()
        sleep(5)



