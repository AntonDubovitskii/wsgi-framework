from anton_framework.templator import render


def index_view(request: dict):
    return '200 OK', render('index.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))


def about_view(request: dict):
    return '200 OK', render('about.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))


def contacts_view(request: dict):
    return '200 OK', render('contacts.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))
