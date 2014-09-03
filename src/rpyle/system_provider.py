import os
import psutil

import chuckbox.log as log
import rpyle.provider as provider


_LOG = log.get_logger(__name__)


class MemoryStatisticsProvider(provider.EntropyProvider, provider.SimpleService):

    def __init__(self):
        self._last = None

    def _get_usage(self):
        memusage = psutil.phymem_usage()
        return (memusage.used, memusage.free)

    def ready(self):
        ready = True
        usage = self._get_usage()

        if self._last is not None:
            same_used = self._last[0] == usage[0]
            same_free = self._last[1] == usage[1]
            ready = not (same_free and same_used)

        return ready

    def available(self):
        return 128

    def read(self, required=0):
        if required == 0:
            return provider.EMPTY_READ

        usage = self._get_usage()
        self._last = usage

        usage_str = ''.join([
            str(usage[0]),
            str(usage[1])
            ])

        if required < len(usage_str):
            return usage_str[:required]
        return usage_str


def is_attribute(obj, name):
    return not name.startswith('_') and not callable(getattr(obj, name))


class CPUStatisticsProvider(provider.EntropyProvider, provider.SimpleService):

    def __init__(self):
        self._last = None

    def _get_usage(self):
        usage = psutil.cpu_times()
        attr_names = [a for a in dir(usage) if is_attribute(usage, a)]

        value = 0
        for attr_name in attr_names:
            attr = getattr(usage, attr_name)

            if isinstance(attr, int) or isinstance(attr, float) or isinstance(attr, long):
                value *= attr

        return (value, )

    def ready(self):
        ready = True
        usage = self._get_usage()

        if self._last is not None:
            ready = not self._last[0] == usage[0]

        return ready

    def available(self):
        return 64

    def read(self, required=0):
        if required == 0:
            return provider.EMPTY_READ

        usage = self._get_usage()
        self._last = usage

        usage_str = str(usage[0])

        if required < len(usage_str):
            return usage_str[:required]
        return usage_str
