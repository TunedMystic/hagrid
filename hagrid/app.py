import json
import time
import uuid

import falcon

from mongoengine.queryset.visitor import Q

from .db import init_db
from .models import Asset


db = None


class Timeit:
    """
    A simple decorator to time functions.
    """

    def __init__(self, fn):
        self.fn = fn

    def format_elapsed(self, elapsed):
        """
        elapsed (float): Time in sec.
        """

        value = elapsed
        unit = 'sec'

        if elapsed < 1:
            value = elapsed * 1000
            unit = 'ms'

        return '{:.3f} {}'.format(value, unit)

    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.fn(*args, **kwargs)
        end = time.time()

        print(self.format_elapsed(end - start))
        return result


def initialize_db():
    global db
    if not db:
        print('[database] initializing')
        db = init_db()
    else:
        print('[database] already initialized!')


initialize_db()


@Timeit
def search(search_text):
    return Asset.objects.filter(Q(name__icontains=search_text) | Q(symbol__startswith=search_text)).scalar('name', 'symbol', 'exchange')[:50]


class UUIDResource:
    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.media = {'uuid': str(uuid.uuid4()), 'source': 'falcon'}


class AssetResource:
    def on_get(self, request, response):
        search_text = request.get_param('q', default='')
        rows = search(search_text)
        serialized_data = [
            {'symbol': r[0], 'name': r[1], 'exchange': r[2]}
            for r in rows
        ]
        response_data = {
            'hits': len(serialized_data),
            'data': serialized_data,
            'source': 'falcon',
        }
        response.status = falcon.HTTP_200
        response.media = response_data


app = falcon.API()

app.add_route('/', UUIDResource())
app.add_route('/assets', AssetResource())
