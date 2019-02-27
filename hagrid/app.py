import uuid

import falcon


class UUIDResource:
    def on_get(self, request, response):
        response.status = falcon.HTTP_200
        response.media = {'uuid': str(uuid.uuid4())}


app = falcon.API()

app.add_route('/', UUIDResource())
