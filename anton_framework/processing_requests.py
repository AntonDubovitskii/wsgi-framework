def parse_input_data(data: str) -> dict:
    """
    Функция получает строку запроса, парсит из неё переданные параметры,
    формирует из них словарь и возвращает его.
    """
    result = {}
    if data:
        params = data.split('&')
        for item in params:
            key, value = item.split('=')
            result[key] = value
    return result


def retrieving_get_request(environ) -> dict:
    """
    Функция получает от сервера словарь environ, находит в нем строку с параметрами GET-запроса,
    передает функции parse_input_data(), после чего возвращает результат.
    """
    query_string = environ['QUERY_STRING']
    request_params = parse_input_data(query_string)
    return request_params


def retrieving_post_request(environ) -> dict:
    """
    Функция получает от сервера словарь environ, считывает из него данные в байтовом формате,
    содержащие параметры POST-запроса, проводит декодирование,
    передает строку функции parse_input_data(), после чего возвращает результат.
    """
    result = {}
    content_length_data = environ.get('CONTENT_LENGTH')
    content_length = int(content_length_data) if content_length_data else 0

    if content_length > 0:
        data = environ['wsgi.input'].read(content_length)
        data_str = data.decode(encoding='utf-8')
        result = parse_input_data(data_str)
    return result





