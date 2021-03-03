import requests
import json


class Exchange:
    exchange_dict = {}

    @staticmethod
    def put_numeric(number):
        new_number = float(number)
        Exchange.exchange_dict['base value'] = new_number

    @staticmethod
    def request(base):
        response = requests.get('https://api.exchangeratesapi.io/latest?base={}'.format(base))
        response_data = json.loads(response.text)
        Exchange.exchange_dict['rate'] = response_data['rates']
        Exchange.exchange_dict['base'] = response_data['base']

    @staticmethod
    def put_transfer_base(transfer_base):
        Exchange.exchange_dict['transfer'] = transfer_base

    @staticmethod
    def get_exchange_data():
        lst = []
        base = Exchange.exchange_dict['base']
        base_value = Exchange.exchange_dict['base value']
        transfer_base = Exchange.exchange_dict['transfer']
        transfer_value = Exchange.exchange_dict['rate'][transfer_base]* base_value
        get_base = '{}:{}'.format(base, format(base_value, '.2f'))
        lst.append(get_base)
        get_transfer_base = '{}:{}'.format(transfer_base, format(transfer_value, '.2f'))
        lst.append(get_transfer_base)
        return lst


