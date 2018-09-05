#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from calendar import monthrange
from datetime import datetime


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


def milliseconds_to_hours(time):
    seconds = int((time/1000) % 60)
    minutes = int((time/(1000*60)) % 60)
    hours = int(time/(1000*60*60))

    return "%02d:%02d:%02d" % (hours, minutes, seconds)


if __name__ == '__main__':

    pass