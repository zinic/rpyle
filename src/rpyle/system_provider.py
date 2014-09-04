import os
import time
import psutil
import subprocess

import chuckbox.log as log
import rpyle.provider as provider


_LOG = log.get_logger(__name__)


def is_pub_attribute(obj, name):
    return not name.startswith('_') and not callable(getattr(obj, name))


class ProcessProvider(provider.EntropyProvider, provider.Service):

    def __init__(self, args):
        self._args = args
        self._subproc = None

    def start(self):

        self._subproc = subprocess.Popen(
            args=self._args,
            stdout=subprocess.PIPE,
            stderr=open(os.devnull, 'a'),
            stdin=open(os.devnull, 'r'))

    def stop(self):
        self._subproc.terminate()

    def ready(self):
        return 4096

    def read(self, required=0):
        return self._subproc.stdout.read(required)


class IntervalProvider(provider.EntropyProvider, provider.SimpleService):

    def __init__(self, interval):
        self._interval = interval
        self._last_read = time.time()

    def ready(self):
        return time.time() - self._last_read > self._interval

    def read(self, required=0):
        self._last_read = time.time()


class MemoryStatisticsProvider(IntervalProvider):

    def __init__(self):
        super(MemoryStatisticsProvider, self).__init__(5)

    def _get_usage(self):
        memusage = psutil.phymem_usage()
        return (memusage.used, memusage.free)

    def available(self):
        return 128

    def read(self, required=0):
        super(MemoryStatisticsProvider, self).read(required)

        if required == 0:
            return provider.EMPTY_READ

        usage = self._get_usage()
        usage_str = ''.join([
            str(usage[0]),
            str(usage[1])])

        return usage_str[:required] if required < len(usage_str) else usage_str


class CPUStatisticsProvider(IntervalProvider):

    def __init__(self):
        super(CPUStatisticsProvider, self).__init__(5)

    def _get_usage(self):
        usage = psutil.cpu_times()
        attr_names = [a for a in dir(usage) if is_pub_attribute(usage, a)]

        value = 0
        for attr_name in attr_names:
            attr = getattr(usage, attr_name)

            if isinstance(attr, int) or isinstance(attr, float) or isinstance(attr, long):
                value += attr

        return value

    def available(self):
        return 64

    def read(self, required=0):
        super(CPUStatisticsProvider, self).read(required)

        if required == 0:
            return provider.EMPTY_READ

        usage = str(int(self._get_usage()))

        return usage[:required] if required < len(usage) else usage
