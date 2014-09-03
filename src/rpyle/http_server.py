import chuckbox.log as log
import wsgiref.simple_server as httpd


_LOG = log.get_logger(__name__)


def serve(app, address='', port=8080):
    server = httpd.make_server(address, port, app)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        _LOG.exception(ex)
