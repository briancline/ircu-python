from ircu import p10


class MessageHandler(p10.MessageHandler):
    token = 'EA'
    command = 'END_OF_BURST_ACK'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def server(self, client, source, args):
        self.logger.info('Burst process complete')
