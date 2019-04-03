#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from class_toggl import TogglClient
import argparse

# togg = TogglClient()
# togg.report_by_client('Bieler', 'LastMonth')

if __name__ == '__main__':

    # clientes = ['Bieler', 'Colombero']
    # tags = ['no-remunerable', 'remunerable']

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('-c', '--client', dest='client', type=str, help='Intrese un cliente')
    parser.add_argument('-d', '--daterange', dest='date_range', type=str,
        choices=['Today', 'Yesterday', 'ThisWeek', 'LastWeek', 'ThisMonth', 'LastMonth'],
        default='LastMonth', help='Selecione un rango de fecha')

    args = parser.parse_args()

    togg = TogglClient()
   
    if args.client is None:
        print("Lista de clientes")
        for t in togg.list_clients():
            print(t['name'])
    else:
        togg.report_by_client(args.client, args.date_range)
