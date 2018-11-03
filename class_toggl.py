#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
import requests
import configparser
from datetime import datetime
from tools import last_month, milliseconds_to_str, taskdatetime_to_datetime, milliseconds_to_hours_decimal


# https://github.com/toggl/toggl_api_docs/blob/master/reports.md

class TogglClient:

    def __init__(self):
        self.version = 1
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.workspace_id = self.config['toggl']['workspace_id']
        self.api_token = self.config['toggl']['api_token']
        self.tag_urgent = self.config['toggl']['tag_urgent']
        self.tag_insitu = self.config['toggl']['tag_insitu']

    def get_data(self, url):
        data = requests.get(url, auth=(self.api_token, 'api_token'))
        return data.json()

    def list_clients(self):
        url = 'https://www.toggl.com/api/v8/workspaces/%s/clients' % self.workspace_id
        clients = []
        for i in self.get_data(url):
            clients.append({
                'id': i['id'],
                'name': i['name']
            })
        return clients

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
        # https://github.com/toggl/toggl_api_docs/blob/master/reports.md#request-parameters
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
        url = 'https://toggl.com/reports/api/v2/details'
        # url = 'https://toggl.com/reports/api/v2/summary'  # Summary report URL

        monthly_summary = {
            'in-situ': {
                'label': 'Horas in-situ (planificada)',
                'value': 0.0  # Horas en decimal
             },
            'in-situ-urgent': {
                'label': 'Horas in-situ (urgentes)',
                'value': 0.0  # Horas en decimal
             },
            'remote': {
                'label': 'Horas remotas (planificada)',
                'value': 0.0  # Horas en decimal
             },
            'remote-urgent': {
                'label': 'Horas remotas (urgentes)',
                'value': 0.0  # Horas en decimal
             },
            'visit': {
                'label': 'Cantidad de visitas (planificada)',
                'value': 0  # Cantidad de visitas
             },
            'visit-urgent': {
                'label': 'Cantidad de visitas (urgentes)',
                'value': 0  # Cantidad de visitas
             }
        }

        # https://github.com/toggl/toggl_api_docs/blob/master/reports.md#request-parameters
        data = self.last_month_common_dataquery()
        data['client_ids'] = self.get_client_id(client)
        data['order_field'] = 'date'
        data['order_desc'] = 'off'

        url_values = urllib.parse.urlencode(data)

        full_url = url + '?' + url_values

        x = self.get_data(full_url)
        # print(x)
        print("\n==== Trabajos realizados ====")
        conunt = 1

        for i in x['data']:
            # Make summary
            if self.tag_insitu in i['tags']:
                if self.tag_urgent in i['tags']:
                    v = self.visit(i['dur'])
                    monthly_summary['visit-urgent']['value'] += v['visit']
                    monthly_summary['in-situ-urgent']['value'] += v['time']
                else:
                    v = self.visit(i['dur'])
                    monthly_summary['visit']['value'] += v['visit']
                    monthly_summary['in-situ']['value'] += v['time']

            else:
                if self.tag_urgent in i['tags']:
                    monthly_summary['remote-urgent']['value'] += milliseconds_to_hours_decimal(i['dur'])

                else:
                    monthly_summary['remote']['value'] += milliseconds_to_hours_decimal(i['dur'])

            stime = milliseconds_to_str(i['dur'])
            dtime = milliseconds_to_hours_decimal(i['dur'])
            task_start = datetime.strftime(taskdatetime_to_datetime(i['start'])[0], "%d/%m/%Y %H:%M")

            print("%s - %s (%s [%sh])" % (task_start, i['description'], stime, dtime))

            # print("%s | %s %s" % (('%02d' % conunt), milliseconds_to_hours(i['time']), i['title']['time_entry']))
            conunt += 1

        print("\n==== Resumen ====")
        for k, v in sorted(monthly_summary.items()):
            print("%-35s = %6.2f" % (v['label'], v['value']))



    def last_month_tag_time(self, tag):
        url = 'https://toggl.com/reports/api/v2/summary'  # Summary report URL

        data = self.last_month_common_dataquery()
        data['tag_ids'] = self.get_tag_id(tag)

        url_values = urllib.parse.urlencode(data)
        full_url = url + '?' + url_values
        # print(full_url)
        x = self.get_data(full_url)

        return milliseconds_to_str(x['total_grand'])


    def visit(self, milliseconds):
        """

        :param milliseconds: Duracion en milisegundos
        :return:
        """
        tasktime = milliseconds_to_hours_decimal(milliseconds)

        if tasktime > 1:
            visit = 1
            rtime = tasktime-1
        else:
            visit = 0
            rtime = tasktime

        data = {
            'visit': visit,
            'time': rtime
        }
        return data
