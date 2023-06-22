from quopri import decodestring
from processing_requests import retrieving_get_request, retrieving_post_request


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    """Основной класс фреймворка."""

    def __init__(self, routes_obj, fronts_obj):
        self.routes = routes_obj
        self.fronts = fronts_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        request = {'method': method}

        if not path.endswith('/'):
            path = f'{path}/'

        if method == 'GET':
            request_params = retrieving_get_request(environ)
            decoded_params = Framework.decode_value(request_params)
            request['request_params'] = decoded_params
            print(f'Получены GET-параметры: {decoded_params}')

        if method == 'POST':
            request_params = retrieving_post_request(environ)
            decoded_params = Framework.decode_value(request_params)
            request['data'] = decoded_params
            print(f'Получены POST-параметры: {decoded_params}')

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data) -> dict:
        new_data = {}
        for k, v in data.items():
            # Добавил еще исправление для ключей, чтобы они тоже отображались правильно
            key = bytes(k.replace('%', '=').replace("+", " "), 'UTF-8')
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            key_decode_str = decodestring(key).decode('UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[key_decode_str] = val_decode_str
        return new_data
