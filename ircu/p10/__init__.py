import logging


class MessageHandler(object):
    token = '?'
    command = '???'

    def __init__(self, *args, **kwargs):
        self.service = kwargs.get('service')
        self.network = kwargs.get('network')
        self.logger = kwargs.get('logger') or logging.getLogger(__name__)

    def unreg(self, client, source, args):
        self.logger.debug('%s ignoring unreg msg', self.token)
        raise NotImplementedError()

    def client(self, client, source, args):
        self.logger.debug('%s ignoring client msg', self.token)
        raise NotImplementedError()

    def server(self, client, source, args):
        self.logger.debug('%s ignoring server msg', self.token)
        raise NotImplementedError()

    def oper(self, client, source, args):
        self.logger.debug('%s ignoring oper msg', self.token)
        raise NotImplementedError()
