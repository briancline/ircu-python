from ircu import consts
from ircu import p10


class MessageHandler(p10.MessageHandler):
    token = 'G'
    command = 'PING'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def server(self, client, source, args):
        # MH G !1469343053.603542 proto.sysnw.net 1469343053.603542
        pong_args = ' '.join(args[2:])
        self.network.send(consts.FMT_PONG, self.service.server.num,
                          source.num, pong_args)
