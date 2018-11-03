#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from class_toggl import TogglClient

if __name__ == '__main__':

    # clientes = ['Bieler', 'Colombero']
    # tags = ['no-remunerable', 'remunerable']

    togg = TogglClient()

    if len(sys.argv) == 2:
        cliente = sys.argv[1]
        togg.last_month_report_by_client(cliente)
    else:
        print("Seleccione un cliente")
        for i in togg.list_clients():
            print(i['name'])

    # for c in clientes:
    #     togg.last_month_report_by_client(c)

    # for tag in tags:
    #     print("%-15s = %s" % (tag, togg.last_month_tag_time(tag)))

