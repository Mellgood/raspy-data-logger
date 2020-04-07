from time import sleep

import peewee as peewee
import psutil as psutil
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


class CpuData(BaseModel):
    temperature = peewee.FloatField()
    uom_temperature = peewee.CharField()
    timestamp_measure = peewee.DateTimeField(default=datetime.datetime.now)
    cpu_percent = peewee.FloatField()
    uom_percent = peewee.CharField()
    cpu_count = peewee.IntegerField()  # psutil.cpu_count()
    cpu_current_frequency = peewee.FloatField()  # psutil.cpu_freq().current
    cpu_min_frequency = peewee.FloatField()  # psutil.cpu_freq().min
    cpu_max_frequency = peewee.FloatField()  # psutil.cpu_freq().max


def init_db():
    try:
        User.create_table()
    except peewee.OperationalError:
        print("User table already exists!")

    try:
        TemperatureMeasure.create_table()
    except peewee.OperationalError:
        print("CpuTemperatures table already exists!")

    try:
        CpuData.create_table()
    except peewee.OperationalError:
        print("CpuData table already exists!")


def get_cpu_temp_measure():
    cpu = CPUTemperature()
    t = TemperatureMeasure()
    t.temperature = float(cpu.temperature)
    t.uom = "°C"
    return t


def get_cpu_data():
    cpu_data = CpuData()
    cpu_data.temperature = CPUTemperature().temperature
    cpu_data.uom_temperature = "°C"
    cpu_data.cpu_percent = psutil.cpu_percent()
    cpu_data.uom_percent = "%"
    cpu_data.cpu_count = psutil.cpu_count()
    cpu_data.cpu_current_frequency = psutil.cpu_freq().current
    cpu_data.cpu_min_frequency = psutil.cpu_freq().min
    cpu_data.cpu_max_frequency = psutil.cpu_freq().max
    return cpu_data


def do_measures():
    t = get_cpu_temp_measure()
    t.save()

    c = get_cpu_data()
    c.save()


def start_loop():
    # just cycle over time. TODO: move configs out of here
    while (True):
        do_measures()
        sleep(5)


if __name__ == '__main__':
    init_db()
    start_loop()




