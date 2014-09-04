import os
import sys
import time
import random
import hashlib
import rpyle.webservice
import rpyle.http_server
import rpyle.system_provider

import chuckbox.log as log
import multiprocessing as mp
import chuckbox.project as project


_LOG = log.get_logger(__name__)


def init():
    log.get_log_manager().configure({
        'level': 'DEBUG',
        'console_enabled': True})

    about= project.about(__package__)
    _LOG.info('About: {}'.format(about.version))

    def start_webapp(randserve):
        app = rpyle.webservice.new_app(randserve)
        rpyle.http_server.serve(app)

    rpyle_server_comm, webserver_comm= mp.Pipe()

    webapp_proc = mp.Process(
        name='ryple_webserver',
        target=start_webapp,
        args=(webserver_comm,))
    webapp_proc.start()

    hasher = hashlib.new('sha1')

    rdata_pool = list()
    rdata_sources = [rpyle.system_provider.ProcessProvider([
            'arecord',
            '-f',
            'dat',
            '-B',
            '1024'
        ]),
        rpyle.system_provider.MemoryStatisticsProvider(),
        rpyle.system_provider.CPUStatisticsProvider()
    ]

    for source in rdata_sources:
        source.start()

    timeout = 0
    default_response = tuple()
    last_display_time = time.time()

    while True:
        entropy_amount = len(rdata_pool)
        if entropy_amount < 262144:
            had_ready_sources = False
            for source in rdata_sources:
                if source.ready():
                    had_ready_sources = True

                    rdata = source.read(64)
                    rdata_pool.extend(rdata)

            if had_ready_sources:
                timeout = 0
            else:
                timeout = 0.1
        else:
            timeout = 1

        now = time.time()
        if now - last_display_time > 7.5:
            last_display_time = now
            _LOG.info('Gathered {} bytes of entropy.'.format(entropy_amount))

        if rpyle_server_comm.poll(timeout):
            request = rpyle_server_comm.recv()
            response = default_response

            if isinstance(request, list) and len(request) > 0:
                command = request[0]

                if command == 'get':
                    if len(rdata_pool) > 128:
                        response = rdata_pool[:128]
                        rdata_pool = rdata_pool[128:]

            rpyle_server_comm.send(response)
