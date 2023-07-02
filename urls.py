from datetime import date

import requests

# from views import index_view, about_view, contacts_view, courses_list_view, category_list_view,\
#     CreateCategory, CreateCourse, copy_course_view


class MoneyFront:
    """Класс, передающий в словарь request данные о курсах валют.
    Если данные получены впервые - кэширует их, впоследствии предоставляет их из кэша."""
    def __init__(self):
        self.cache = {}

    def __call__(self, request: dict):
        if 'exchange_rate' in self.cache:
            request['exchange_rate'] = self.cache['exchange_rate']
            print('Данные о курсе валют получены из кэша')
        else:
            url = f'https://www.cbr-xml-daily.ru/daily_json.js'
            data = requests.get(url).json()
            usd_exchange_rate = round(data['Valute']['USD']['Value'], 2)
            euro_exchange_rate = round(data['Valute']['EUR']['Value'], 2)
            print('Данные о курсе валют получены через обращение к внешнему ресурсу')

            self.cache['exchange_rate'] = {'us_dollar': usd_exchange_rate, 'euro': euro_exchange_rate}
            request['exchange_rate'] = {'us_dollar': usd_exchange_rate, 'euro': euro_exchange_rate}


def date_front(request: dict):
    """Функция сохраняет в request текущую дату."""
    request['date'] = date.today()


fronts = [date_front, MoneyFront()]

# routes = {
#     '/': index_view,
#     '/about/': about_view,
#     '/contacts/': contacts_view,
#     '/category-list/': category_list_view,
#     '/courses-list/': courses_list_view,
#     '/create-course/': CreateCourse(),
#     '/create-category/': CreateCategory(),
#     '/copy-course/': copy_course_view
# }
