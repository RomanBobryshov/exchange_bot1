import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os


class Diagram:
    diagram_dict = {}

    @staticmethod
    def put_base(base):
        Diagram.diagram_dict['base'] = base

    @staticmethod
    def put_transfer(transfer_base):
        Diagram.diagram_dict['transfer_base'] = transfer_base

    @staticmethod
    def request():
        date_now = datetime.now()
        format_date = datetime.strftime(date_now, "%Y.%m.%d").replace('.', '-')
        past_date = date_now - timedelta(days=7)
        format_past_date = datetime.strftime(past_date, "%Y.%m.%d").replace('.', '-')
        base = Diagram.diagram_dict['base']
        transfer_base = Diagram.diagram_dict['transfer_base']
        try :
            response = requests.get('https://api.exchangeratesapi.io/history?start_at={}&end_at={}&base={}&symbols={}'
                                    .format(format_past_date, format_date, base, transfer_base))
        except:
            error = ' No exchange rate data is available for the selected currency.'
            Diagram.get_error(error)
        else:
            response_data = json.loads(response.text)
            Diagram.get_diagrams_lists(response_data)

    @staticmethod
    def get_error(error):
        lst = []
        result = lst.append(error)
        return result

    @staticmethod
    def get_diagrams_lists(respons_data):
        dates = respons_data['rates'].keys()
        list_dates = []
        for el in dates:
            list_dates.append(el)
        transfer_base = Diagram.diagram_dict['transfer_base']
        values = respons_data['rates'].values()
        list_values = []
        for el in values:
            list_values.append(el[transfer_base])
        Diagram.save_diagram(sorted(list_dates), list_values)

    @staticmethod
    def save_diagram(list_dates, list_values):
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='white', dpi=80)
        lim = sorted(list_values)
        lim_delta = lim[1] - lim[0]
        ax.set_title(Diagram.diagram_dict['transfer_base'])
        ax.set(ylabel='values', ylim=(lim[0] - lim_delta, lim[-1] + lim_delta))
        plt.bar(list_dates, list_values)
        fig.savefig('diagrams/{}'.format(Diagram.diagram_dict['transfer_base']))

    @staticmethod
    def dell_diagram():
        os.remove('diagrams/{}.png'.format(Diagram.diagram_dict['transfer_base']))


