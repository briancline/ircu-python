import unittest

import six.moves

try:
    import mock
except ImportError:
    import unittest.mock as mock

from ircu import network
from ircu import server
from ircu import service
from ircu import util


CONF = """
[uplink]
timeout = 1.0

[server]
numeric = 3502
name = unit.ircplanet.net
info = This is not a pipe
modes = sh
max_clients = 262144

[bot]
numeric = 42
nick = unittest
ident = unit
host = unit.ircplanet.net
info = Unit Test Bot
ip = 0.0.0.0
modes =
"""


def mock_open(fn, *args, **kwargs):
    # mock.mock_open is broken with a StopIteration that bubbles up too far,
    # and they're in no hurry to fix it: https://bugs.python.org/issue21258
    return six.moves.StringIO(CONF)


class TestService(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_basic(self):
        with mock.patch('ircu.util.open', mock_open):
            conf = util.load_config('unit.ini')

        s = service.Service(conf)
        self.assertIsInstance(s.server, server.Server)
        self.assertIsInstance(s.network, network.Network)
