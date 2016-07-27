from ircu import p10


class MessageHandler(p10.MessageHandler):
    token = 'N'
    command = 'NICK'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def server(self, client, source, args):

    def client(self, client, source, args):
        self.logger.info('nick change by %s', client)
