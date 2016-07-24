from ircu import p10


class MessageHandler(p10.MessageHandler):
    token = 'N'
    command = 'NICK'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def server(self, client, source, args):
        self.logger.info('new user %s from server %s', args[2], source)

    def client(self, client, source, args):
        self.logger.info('nick change by %s', client)
