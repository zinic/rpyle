import os
import json
import base64
import falcon

import chuckbox.log as log


_LOG = log.get_logger(__name__)


def new_app(randserve):
    # Where are we?
    cwd = os.path.realpath(os.getcwd())
    src_dir = os.path.join(cwd, 'src')
    site_dir = os.path.join(src_dir, 'site')

    # falcon.API instances are callable WSGI apps
    app = falcon.API()
    app.add_route('/rand', RandomResource(randserve))
    app.add_route('/roller', RollerResource(site_dir))
    app.add_route('/roller/{path}', RollerResource(site_dir))

    return app


class RollerResource(object):

    def __init__(self, http_path):
        self.http_path = http_path

    def on_get(self, req, resp, path=''):
        resp.status = '404 NOT FOUND'

        file_requested = path if path != '' or path == '/' else 'index.html'
        target = os.path.join(self.http_path, file_requested)

        if os.path.exists(target):
            resp.status = '200 OK'

            if target.endswith('.html'):
                resp.set_header('Content-Type', 'text/html')
            elif target.endswith('.js'):
                resp.set_header('Content-Type', 'text/javascript')
            else:
                resp.set_header('Content-Type', 'text/plain')

            resp.body = open(target, 'r').read()


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
                        'content': base64.b64encode(''.join(rdata))
                    })
                else:
                    resp.status = '503 AWAITING ENTROPY'
