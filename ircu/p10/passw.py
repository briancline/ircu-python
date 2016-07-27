from ircu import p10


class MessageHandler(p10.MessageHandler):
    token = 'PA'
    command = 'PASS'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def unreg(self, client, source, args):
        passwd = args[0]
        if passwd != self.service.conf.get('uplink', 'password'):
            raise ValueError('Password from uplink does not match config')
