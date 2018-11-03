#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from calendar import monthrange
from datetime import datetime
import re

def last_month():
    """
    Devuelve la fecha en formto 'YYY-MM-DD' del comienzo y el fin del mes anterior
    :return:
    """
    now = datetime.now()
    year = now.year
    month = now.month - 1
    start = "%04d-%02d-%02d" % (year, month, 1)
    end = "%04d-%02d-%02d" % (year, month, monthrange(year, month)[1])
    return {
        'start': start,
        'end': end
    }


def this_month():
    """
    Devuelve la fecha en formto 'YYY-MM-DD' del comienzo y el fin del mes anterior
    :return:
    """
    now = datetime.now()
    year = now.year
    month = now.month - 1
    start = "%04d-%02d-%02d" % (year, month, 1)
    end = "%04d-%02d-%02d" % (year, month, monthrange(year, month)[1])
    return {
        'start': start,
        'end': end
    }


def milliseconds_to_str(milliseconds):
    """

    :param milliseconds:
    :return: string %02d:%02d:%02d
    """
    seconds = int((milliseconds/1000) % 60)
    minutes = int((milliseconds/(1000*60)) % 60)
    hours = int(milliseconds/(1000*60*60))
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


def milliseconds_to_minutes(milliseconds):
    """

    :param milliseconds:
    :return: integer - total de minutos
    """
    minutes = int(milliseconds / (1000 * 60))
    return minutes


def milliseconds_to_hours_decimal(milliseconds):
    """

    :param milliseconds: Integer
    :return: decimal - Horas en formato decimal.
    """

    minutes = int((milliseconds / (1000 * 60)) % 60)
    hours = int(milliseconds / (1000 * 60 * 60))

    decimal = hours + (minutes/60.0)

    return round(decimal, 2)


def taskdatetime_to_datetime(stringtime):
    """
    Input string  "2018-10-11T11:02:40-03:00"
    :param stringtime:
    :return:
    """

    timepattern = "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    tzpattern = "[+|-]{1}\d{2}:\d{2}"

    tasktime = datetime.strptime(re.findall(timepattern, stringtime)[0], "%Y-%m-%dT%H:%M:%S")
    tasktz = re.findall(tzpattern, stringtime)[0], "%Y-%m-%dT%H:%M:%S"

    return tasktime, tasktz


if __name__ == '__main__':

    pass