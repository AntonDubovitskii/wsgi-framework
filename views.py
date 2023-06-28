from anton_framework.templator import render
from patterns.creational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class CreateCategory:
    def __call__(self, request: dict):

        if request['method'] == 'POST':

            category = None
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('category_list.html', obj_list=site.categories, date=request.get('date', None),
                                    exchange_rate=request.get('exchange_rate'))
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories, date=request.get('date', None),
                                    exchange_rate=request.get('exchange_rate'))


class CreateCourse:
    category_id = -1

    def __call__(self, request: dict):
        if request['method'] == 'POST':
            category = None

            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            course_format = data['format']
            course_format = site.decode_value(course_format)

            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course(course_format, name, category)
                site.courses.append(course)

            return '200 OK', render('courses_list.html',
                                    obj_list=category.courses, name=category.name, id=category.id,
                                    date=request.get('date', None),
                                    exchange_rate=request.get('exchange_rate'))

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id,
                                        date=request.get('date', None), exchange_rate=request.get('exchange_rate'))
            except KeyError:
                return '200 OK', 'Отсутствуют программы обучения'


def index_view(request: dict):
    return '200 OK', render('index.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))


def about_view(request: dict):
    return '200 OK', render('about.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))


def contacts_view(request: dict):
    return '200 OK', render('contacts.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))


def category_list_view(request: dict):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'), obj_list=site.categories)


def courses_list_view(request: dict):
    logger.log('Список курсов')
    try:
        category = site.find_category_by_id(
            int(request['request_params']['id']))
        return '200 OK', render('courses_list.html', date=request.get('date', None),
                                exchange_rate=request.get('exchange_rate'), obj_list=category.courses,
                                name=category.name, id=category.id)
    except KeyError:
        return '200 OK', 'На данный момент актуальных курсов нет'


def copy_course_view(request: dict):
    request_params = request['request_params']
    category = site.find_category_by_id(int(request['request_params']['id']))

    try:
        name = request_params['name']

        old_course = site.get_course(name)
        if old_course:
            new_name = f'{name}-копия'
            new_course = old_course.clone()
            new_course.name = new_name
            site.courses.append(new_course)
            # Приходится добавлять курс категории вручную, так как стандартный механизм в данном случае не работает
            category.courses.append(new_course)

        return '200 OK', render('courses_list.html',
                                obj_list=site.courses, date=request.get('date', None),
                                exchange_rate=request.get('exchange_rate'),
                                name=new_course.category.name)
    except KeyError:
        return '200 OK', 'No courses have been added yet'

