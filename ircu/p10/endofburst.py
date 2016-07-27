from ircu import consts
from ircu import p10


class MessageHandler(p10.MessageHandler):
    token = 'EB'
    command = 'END_OF_BURST'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def server(self, client, source, args):
        # MH EB
        self.network.send(consts.FMT_ENDOFBURST_ACK,
                          self.service.server.num)
