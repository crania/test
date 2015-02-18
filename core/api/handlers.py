import json
from tornado.web import RequestHandler
from tornado import gen
import random

from .models import DDBHits


class IndexHandler(RequestHandler):

    def get(self):
        self.write('It works.')

class HitsHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        limit = self.get_argument('limit', 10)
        last = self.get_argument('last', None)
        hit = DDBHits()
        e = yield hit.items(limit=limit, last=last)
        self.write(json.dumps(e))


class HitHandler(RequestHandler):

    @gen.coroutine
    def get(self, hit_id):
        hit = DDBHits()
        e = yield hit.get(hit_id=hit_id)
        self.write(json.dumps(e))

    @gen.coroutine
    def put(self, hit_id):
        from datetime import datetime
        print self.request.hit_id

        # returns 201 if created or 200 if modified

        data = json.loads(self.request.body)
        #data = yaml.load(self.request.body)
        data['page_name'] = page_name
        data['hit_date'] = datetime.now().strftime('%y%m%d%H%M%S:%f')
        data['hit_id'] = self.get_argument("hit_id")
        print data
        hit = DDBHits()

        e = yield hit.create(**data)
        self.write(json.dumps(e))


    @gen.coroutine
    def delete(self, hit_id):
        hit = DDBHits()
        e = yield hit.delete(hit_id=hit_id)
        self.write(json.dumps(e))

class RandomHitsHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        hit = DDBHits()
        e = yield hit.get(hit_id=str(random.randrange(1, 1000000)))
        self.write(json.dumps(e))


class SearchHitsHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        limit = self.get_argument('limit', 10)
        last = self.get_argument('last', None)
        q = self.get_argument('q')
        hit = DDBHits()
        e = yield hit.search(limit=limit, last=last, q=q)
        self.write(json.dumps(e))


'''
class EpisodesHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        limit = self.get_argument('limit', 10)
        last = self.get_argument('last', None)
        episode = DDBEpisode()
        e = yield episode.items(limit=limit, last=last)
        self.write(json.dumps(e))


class EpisodeHandler(RequestHandler):

    @gen.coroutine
    def get(self, number):
        episode = DDBEpisode()
        e = yield episode.get(number=number)
        self.write(json.dumps(e))

    @gen.coroutine
    def put(self, number):
        # returns 201 if created or 200 if modified
        data = json.loads(self.request.body)
        data['number'] = number
        episode = DDBEpisode()
        e = yield episode.create(**data)
        self.write(json.dumps(e))

    @gen.coroutine
    def delete(self, number):
        episode = DDBEpisode()
        e = yield episode.delete(number=number)
        self.write(json.dumps(e))


class SearchHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        limit = self.get_argument('limit', 10)
        last = self.get_argument('last', None)
        q = self.get_argument('q')
        episode = DDBEpisode()
        e = yield episode.search(limit=limit, last=last, q=q)
        self.write(json.dumps(e)) '''
