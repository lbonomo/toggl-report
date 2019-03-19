#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from class_toggl import TogglClient
import argparse


if __name__ == '__main__':

    # clientes = ['Bieler', 'Colombero']
    # tags = ['no-remunerable', 'remunerable']



    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('-t', '--tag', dest='tag', type=str, help='Tag')
    parser.add_argument('-d', '--daterange', dest='date_range', type=str,
        choices=['Today', 'Yesterday', 'ThisWeek', 'LastWeek', 'ThisMonth', 'LastMonth'],
        default='LastMonth', help='Selecione un rango de fecha')

    args = parser.parse_args()

    togg = TogglClient()

    if args.tag is None:
        for t in togg.list_tags():
            print(t['name'])
    else:
        print(togg.report_by_tag_totaltime(args.tag, args.date_range))


