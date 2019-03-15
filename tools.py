#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from calendar import monthrange
from datetime import datetime, date, timedelta
import re


def get_date_range(date_trange):
    """
    Devuelve la fecha en formto 'YYY-MM-DD' del comienzo y el fin del mes anterior
    :return:
    """

    now = datetime.now()
    today = date.today()
    doy = today.timetuple().tm_yday
    (iso_year, iso_weeknumber, iso_weekday) = today.isocalendar()
    yesterday = today - timedelta(days=1)
    this_year = now.year
    this_month = now.month
    last_year = now.year - 1
    last_month = now.month - 1

    if (date_trange == "LastMonth"):
        if (doy == 1):
            start = "%04d-%02d-%02d" % (this_year-1, 12, 1)
            end = "%04d-%02d-%02d" % (this_year-1, 12, 31)
        else:
            start = "%04d-%02d-%02d" % (this_year, last_month, 1)
            end = "%04d-%02d-%02d" % (this_year, last_month, monthrange(this_year, last_month)[1])

    if (date_trange == "ThisMonth"):
        start = "%04d-%02d-%02d" % (this_year, this_month, 1)
        end = "%04d-%02d-%02d" % (this_year, this_month, monthrange(this_year, this_month)[1])

    if (date_trange == "Today"):
        start = today.strftime('%Y-%m-%d')
        end = start

    if (date_trange == "Yesterday"):
        start = yesterday.strftime('%Y-%m-%d')
        end = start

    if (date_trange == "ThisWeek"):
        startweek = today - timedelta(days=iso_weekday)
        start = startweek.strftime('%Y-%m-%d')
        end = (startweek + timedelta(days=6)).strftime('%Y-%m-%d')

    if (date_trange == "LastWeek"):
        startweek = today - timedelta(days=( iso_weekday + 7))
        start = startweek.strftime('%Y-%m-%d')
        end = (startweek + timedelta(days=6)).strftime('%Y-%m-%d')

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
