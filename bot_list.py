import sqlite3
import requests
import json


def sqlite_3_update(rates, base):
    con = sqlite3.connect('exchange_bot.db')
    data = [base, str(rates)]
    con.execute("INSERT INTO exchange VALUES(?,?,time('now'))", data)
    con.commit()


def sqlite_3_select(base):
    current_base = base
    con = sqlite3.connect('exchange_bot.db')
    cur = con.cursor()
    cur.execute("SELECT base FROM EXCHANGE WHERE base = ?", (current_base,))
    exists = cur.fetchall()
    if not exists:
        request(base)
    cur.execute("SELECT rate FROM EXCHANGE WHERE base = (?) and time > time('now', '- 10 minute')", (current_base,))
    exists2 = cur.fetchall()
    if not exists2:
        request(current_base)
        sqlite_3_dell(current_base)
    else:
        exists2_list = exists2[0][0]
        rates = eval(exists2_list)
        Rates.rates(rates, current_base)


def sqlite_3_dell(base):
    con = sqlite3.connect('exchange_bot.db')
    cur = con.cursor()
    cur.execute("DELETE from EXCHANGE where base = ?", (base,))
    con.commit()


def request(base):
    response = requests.get('https://api.exchangeratesapi.io/latest?base={}'.format(base))
    response_data = json.loads(response.text)
    Rates.rates(response_data['rates'], base)
    return sqlite_3_update(response_data['rates'], base)


class Rates:
    new_dict = {}

    @staticmethod
    def rates(rates, base):
        if base in rates:
            del rates[base]
        rates_list = list(rates.items())[0:20]
        return Rates.new_dict.update(rates_list)

    @staticmethod
    def get_rates():
        lst = []
        for el1, el2 in Rates.new_dict.items():
            el2 = format(el2, '.2f')
            get_rate = '{}:{}'.format(el1, el2)
            lst.append(get_rate)
        return lst





