from ircu import consts


class Network(object):
    def __init__(self, service=None):
        self.service = service
        self.servers = {}
        self.users = {}

    def send(self, msg, *args):
        line = msg % tuple(args)
        self.service.send_queue.append(line)

    def resolve_numeric(self, num):
        num_len = len(num)
        if num_len == consts.BASE64_SERVLEN:
            src = self.servers.get(num)
        elif num_len == (consts.BASE64_SERVLEN + consts.BASE64_USERLEN):
            src = self.users.get(num)
        else:
            raise ValueError('Unknown numeric: %r' % num)

        return src
