import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from handlers.patterns import url_patterns
from restful_api.resource_handlers import ResourceHandlers

from restful.rest import RestService

define('port', default=80, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            login_url='/login',
            cookie_secret='MuG7xxacQdGPR7Svny1OfY6AymHPb0H/t02+I8rIHHE=',
        )
        super(Application, self).__init__(url_patterns, **settings)

def GetRestfulApp():
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
        login_url='/login',
        cookie_secret='MuG7xxacQdGPR7Svny1OfY6AymHPb0H/t02+I8rIHHE=',
    )
    return RestService(ResourceHandlers, handlers=url_patterns, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(GetRestfulApp())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
