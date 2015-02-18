from core.common.utils import rel
from core.api.handlers import (
    IndexHandler, HitsHandler, HitHandler,
    SearchHitsHandler,RandomHitsHandler)
from core.api.models import DDBHits
from os import environ
from tornado import web, options, ioloop


ENV = environ.get('BEBOP_ENV', 'dev')


class HitsApplication(web.Application):

    def __init__(self, **kwargs):
        DDBHits().create_table_if_not_exists()
        kwargs['handlers'] = [
            web.url(r'/', IndexHandler, name='index'),
            web.url(r'/hits', HitsHandler, name='hits'),
            web.url(r'/hit/(.*)', HitHandler, name='hit'),
            web.url(r'/search', SearchHitsHandler, name='search'),
            web.url(r'/random', RandomHitsHandler, name='random'),
        ]
        kwargs['debug'] = True
        super(HitsApplication, self).__init__(**kwargs)


if __name__ == '__main__':
    options.parse_command_line()
    # see bebop/common/__init__.py
    options.parse_config_file(rel('config/{env}.cfg'.format(env=ENV)))

    application = HitsApplication()
    application.listen(options.options.port)
    ioloop.IOLoop.instance().start()
