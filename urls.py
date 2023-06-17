from datetime import date

import requests

from views import index_view, about_view, contacts_view


def date_front(request: dict):
    """Функция сохраняет в request текущую дату."""
    request['date'] = date.today()


def money_front(request: dict):
    """
    Функция парсит информацию о курсе валют и сохраняет в виде словаря в request.
    :param request:
    :return:
    """
    url = f'https://www.cbr-xml-daily.ru/daily_json.js'
    data = requests.get(url).json()
    usd_exchange_rate = round(data['Valute']['USD']['Value'], 2)
    euro_exchange_rate = round(data['Valute']['EUR']['Value'], 2)

    request['exchange_rate'] = {'us_dollar': usd_exchange_rate, 'euro': euro_exchange_rate}


fronts = [date_front, money_front]

routes = {
    '/': index_view,
    '/about/': about_view,
    '/contacts/': contacts_view,
}
