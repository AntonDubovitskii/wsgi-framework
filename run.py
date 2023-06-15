from wsgiref.simple_server import make_server

from anton_framework.main import Framework
from urls import routes, fronts

application = Framework(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Serving on port 8080...")
    httpd.serve_forever()
