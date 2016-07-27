from ircu import p10
from ircu import server
from ircu import util


class MessageHandler(p10.MessageHandler):
    token = 'S'
    command = 'SERVER'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def unreg(self, client, source, args):
        # newton.ircplanet.net 1 1469157290 1469171915 J10 MHAD] +h6 :a server
        svr_num, max_conn = util.parse_server_num_maxconn(args[5])

        svr = server.Server(numeric=svr_num,
                            name=args[0],
                            info=args[7],
                            max_clients=max_conn,
                            num_hops=int(args[1]),
                            boot_time=int(args[2]),
                            link_time=int(args[3]),
                            proto=args[4],
                            modes=args[6])
        self.network.servers[svr_num] = svr
        self.service.uplink = self.network.servers[svr_num]

    def server(self, client, source, args):
        # AE S services.ircplanet.net 2 0 1116989941 P10 M[AB] +s :a server
        svr_num, max_conn = util.parse_server_num_maxconn(args[7])

        svr = server.Server(numeric=svr_num,
                            name=args[0],
                            info=args[7],
                            max_clients=max_conn,
                            num_hops=int(args[1]),
                            boot_time=int(args[2]),
                            link_time=int(args[3]),
                            proto=args[4],
                            modes=args[6])
        self.network.servers[svr_num] = svr
