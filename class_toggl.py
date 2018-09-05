#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
import requests
import configparser
from tools import last_month, milliseconds_to_hours


# https://github.com/toggl/toggl_api_docs/blob/master/reports.md

class TogglClient:

    def __init__(self):
        self.version = 1
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.workspace_id = self.config['toggl']['workspace_id']
        self.api_token = self.config['toggl']['api_token']

    def get_data(self, url):
        data = requests.get(url, auth=(self.api_token, 'api_token'))
        return data.json()

    def get_client_id(self, client_name):
        url = 'https://www.toggl.com/api/v8/workspaces/%s/clients' % self.workspace_id

        for i in self.get_data(url):
            if i['name'] == client_name:
                cliente_id = i['id']
                break
            else:
                cliente_id = False

        return cliente_id

    def get_tag_id(self, tag_name):
        url = 'https://www.toggl.com/api/v8/workspaces/%s/tags' % self.workspace_id

        for i in self.get_data(url):
            if i['name'] == tag_name:
                tag_id = i['id']
                break
            else:
                tag_id = False

        return tag_id

    def last_month_common_dataquery(self):
        data = {}
        data['page'] = 1
        data['user_agent'] = "Vanguard Toggl Report"
        data['workspace_id'] = self.workspace_id
        data['since'] = last_month()['start']
        data['until'] = last_month()['end']
        data['order_field'] = 'amount'

        return data

    def last_month_report_by_client(self, client):
        """
        Reporte de horas trabajadas por clientes
        :param client:
        :return:
        """

        url = 'https://toggl.com/reports/api/v2/summary'  # Summary report URL

        data = self.last_month_common_dataquery()
        data['client_ids'] = self.get_client_id(client)

        url_values = urllib.parse.urlencode(data)

        full_url = url + '?' + url_values

        x = self.get_data(full_url)

        print("Trabajos realizados")
        conunt = 1
        for i in x['data'][0]['items']:
            print("%s | %s %s" % (('%02d' % conunt), milliseconds_to_hours(i['time']), i['title']['time_entry']))
            conunt += 1

        print("Total de horas trabajadas: %s\n" % milliseconds_to_hours(x['data'][0]['time']))

    def last_month_tag_time(self, tag):
        url = 'https://toggl.com/reports/api/v2/summary'  # Summary report URL

        data = self.last_month_common_dataquery()
        data['tag_ids'] = self.get_tag_id(tag)

        url_values = urllib.parse.urlencode(data)
        full_url = url + '?' + url_values
        # print(full_url)
        x = self.get_data(full_url)

        return milliseconds_to_hours(x['total_grand'])

