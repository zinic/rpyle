EMPTY_READ = tuple()
MAX_READ_WINDOW = 4096


class Service(object):

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()


class SimpleService(Service):

    def start(self):
        pass

    def stop(self):
        pass


class AsyncService(Service):

    def start(self):
        pass

    def stop(self):
        pass


class EntropyProvider(Service):

    def ready(self):
        raise NotImplementedError()

    def available(self):
        raise NotImplementedError()

    def read(self, required=0):
        raise NotImplementedError()
