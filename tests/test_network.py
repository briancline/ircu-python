import unittest

from ircu import network


class TestNetwork(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_network_init(self):
        network.Network()
