#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from class_toggl import TogglClient

if __name__ == '__main__':

    clientes = ['Bieler', 'Colombero']
    tags = ['no-remunerable', 'remunerable']

    togg = TogglClient()

    for c in clientes:
        togg.last_month_report_by_client(c)

    for tag in tags:
        print("%-15s = %s" % (tag, togg.last_month_tag_time(tag)))

