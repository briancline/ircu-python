import unittest

from ircu import server


SVR_NUM = 3502
SVR_NUM_STR = '2u'
SVR_NAME = 'unit.ircplanet.net'
SVR_INFO = 'This is not a pipe'
SVR_MAX_CLIENTS = 262144
SVR_UPLINK = 'SH'
SVR_HOPS = 1
SVR_HOPS_UPLINK = 0
SVR_BOOT_TS = 1123581321
SVR_LINK_TS = 1234567890
SVR_PROTO = 'P10'
SVR_PROTO_UPLINK = 'J10'
SVR_FLAGS = '+s'
SVR_FLAGS_UPLINK = '+hs'

CONF = {
    'name': 'ircPlanet',
    'server_num': SVR_NUM,
    'server_name': SVR_NAME,
}


class TestServer(unittest.TestCase):
    def test_server_basic(self):
        svr = server.Server(SVR_NUM_STR, SVR_NAME, SVR_INFO, SVR_MAX_CLIENTS,
                            SVR_UPLINK, SVR_HOPS, SVR_BOOT_TS, SVR_LINK_TS,
                            SVR_PROTO_UPLINK, SVR_FLAGS)
        self.assertEqual(svr.num.int, SVR_NUM)
        self.assertEqual(str(svr.num), SVR_NUM_STR)
        self.assertEqual(svr.name, SVR_NAME)
        self.assertEqual(svr.info, SVR_INFO)
        self.assertEqual(svr.max_clients, SVR_MAX_CLIENTS)
