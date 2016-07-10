import unittest

from ircu import network
from ircu import server
from ircu import service


SVR_NUM = '3502'
SVR_NUM_STR = '2u'
SVR_NAME = 'unit.ircplanet.net'
SVR_INFO = 'This is not a pipe'
SVR_MAX_CLIENTS = 262144

CONF = {
    'name': 'ircPlanet',
    'server_num': SVR_NUM,
    'server_name': SVR_NAME,
    'server_info': SVR_INFO,
    'max_clients': SVR_MAX_CLIENTS,
}


class TestService(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_basic(self):
        s = service.Service(CONF)
        self.assertIsInstance(s.server, server.Server)
        self.assertIsInstance(s.network, network.Network)
