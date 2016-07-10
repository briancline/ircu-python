from ircu import network
from ircu import server


class Service(object):
    def __init__(self, conf):
        self.config = conf
        self.network = network.Network()
        self.server = server.Server(
            numeric=int(conf.get('server_num')),
            name=conf.get('server_name'),
            info=conf.get('server_info'),
            max_clients=conf.get('max_clients'))
