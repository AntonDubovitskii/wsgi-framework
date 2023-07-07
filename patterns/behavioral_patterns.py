from jsonpickle import dumps, loads
from anton_framework.templator import render


# Паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self, request):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self, request):
        template_name = self.get_template()
        context = self.get_context_data(request)
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context(request)


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'obj_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self, request):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


class DeleteView(TemplateView):
    template_name = 'delete.html'
    queryset = []
    context_object_name = 'obj_list'

    def get_queryset(self, mapper=None):
        return self.queryset

    @staticmethod
    def get_request_data(request):
        return request['data']

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self, request):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context

    def delete_obj(self, data, mapper=None):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.delete_obj(data)

            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


class ChangeView(TemplateView):
    template_name = 'change.html'
    queryset = []
    context_object_name = 'obj_list'

    def get_queryset(self, mapper=None):
        return self.queryset

    @staticmethod
    def get_request_data(request):
        return request['data']

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self, request):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context

    def change_obj(self, data, mapper=None):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.change_obj(data)

            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


# Паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


# Паттерн - Наблюдатель
class Observer:

    def update(self, subject):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):
    def update(self, subject):
        print(f'Сообщение через СМС: "К нам присоединился {subject.students[-1].name}"')


class EmailNotifier(Observer):
    def update(self, subject):
        print(f'Сообщение через EMAIL: "К нам присоединился {subject.students[-1].name}"')


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)
