import json
import falcon

import chuckbox.log as log


_LOG = log.get_logger(__name__)


def new_app(randserve):
    # falcon.API instances are callable WSGI apps
    app = falcon.API()

    rand_resource = RandomResource(randserve)
    app.add_route('/rand', rand_resource)

    return app


class RandomResource(object):

    def __init__(self, randserve):
        self._randserve= randserve

    def on_get(self, req, resp):
        resp.status = '501 INTERNAL SERVER ERROR'

        self._randserve.send(['get'])

        if self._randserve.poll(1):
            rdata = self._randserve.recv()
            
            if isinstance(rdata, list) or isinstance(rdata, tuple):
                if len(rdata) > 0:
                    resp.status = '200 OK'
                    resp.set_header('Content-Type', 'application/json')
                    resp.body = json.dumps({
                        'content': str(rdata)
                    })
                else:
                    resp.status = '503 AWAITING ENTROPY'
