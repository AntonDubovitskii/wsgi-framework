from anton_framework.templator import render
from behavioral_patterns import ListView, CreateView, BaseSerializer, EmailNotifier, SmsNotifier, FileWriter, \
    DeleteView, ChangeView
from patterns.creational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import app_route, AppRoute, debug_func, DebugClass
from architectural_patterns import UnitOfWork

site = Engine()

logger = Logger('main', FileWriter())

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

routes = {}


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @DebugClass(name='CreateCategory')
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


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @DebugClass(name='CreateCourse')
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

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

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


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['date'] = request.get('date', None)
        context['exchange_rate'] = request.get('exchange_rate')
        return context


@AppRoute(routes=routes, url='/create-student/')
class AddStudentView(CreateView):
    template_name = 'create_student.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['date'] = request.get('date', None)
        context['exchange_rate'] = request.get('exchange_rate')
        return context

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/delete-student/')
class DeleteStudentView(DeleteView):
    template_name = 'delete_student.html'
    mapper = MapperRegistry.get_current_mapper('student')

    def get_queryset(self, mapper=mapper):
        return mapper.all()

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['date'] = request.get('date', None)
        context['exchange_rate'] = request.get('exchange_rate')
        return context

    def delete_obj(self, data: dict, mapper=mapper):
        student_id = data['student_id']
        student_id = site.decode_value(student_id)
        del_obj = mapper.find_by_id(student_id)
        del_obj.mark_removed()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/change-student/')
class ChangeStudentView(ChangeView):
    template_name = 'change_student.html'
    mapper = MapperRegistry.get_current_mapper('student')

    def get_queryset(self, mapper=mapper):
        return mapper.all()

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['date'] = request.get('date', None)
        context['exchange_rate'] = request.get('exchange_rate')
        return context

    def change_obj(self, data: dict, mapper=mapper):
        student_id = data['student_id']
        student_id = site.decode_value(student_id)
        new_name = data['new_name']
        new_name = site.decode_value(new_name)
        change_obj = mapper.find_by_id(student_id)
        change_obj.name = new_name
        change_obj.mark_dirty()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class EnrollStudentToCourseView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['courses'] = site.courses
        context['students'] = site.students
        context['date'] = request.get('date', None)
        context['exchange_rate'] = request.get('exchange_rate')
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @DebugClass(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()


@app_route(routes=routes, url='/')
@debug_func(name='Index')
def index_view(request: dict):
    logger.log('Открыта главная страница')
    return '200 OK', render('index.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))


@app_route(routes=routes, url='/about/')
@debug_func(name='About')
def about_view(request: dict):
    logger.log('Открыта страница "О нас"')
    return '200 OK', render('about.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))


@app_route(routes=routes, url='/contacts/')
@debug_func(name='Contacts')
def contacts_view(request: dict):
    logger.log('Открыта страница "Контакты"')
    return '200 OK', render('contacts.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'))


@app_route(routes=routes, url='/category-list/')
def category_list_view(request: dict):
    logger.log('Открыт список категорий')
    return '200 OK', render('category_list.html', date=request.get('date', None),
                            exchange_rate=request.get('exchange_rate'), obj_list=site.categories)


@app_route(routes=routes, url='/courses-list/')
def courses_list_view(request: dict):
    logger.log('Открыт список курсов')
    try:
        category = site.find_category_by_id(
            int(request['request_params']['id']))
        return '200 OK', render('courses_list.html', date=request.get('date', None),
                                exchange_rate=request.get('exchange_rate'), obj_list=category.courses,
                                name=category.name, id=category.id)
    except KeyError:
        return '200 OK', 'На данный момент актуальных курсов нет'


@app_route(routes=routes, url='/copy-course/')
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


if __name__ == '__main__':
    print(routes)
