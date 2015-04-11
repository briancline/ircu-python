import unittest

from ircu import consts
from ircu import util


class TestBase64(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        self.assertIsNotNone(consts.version_str)
        self.assertGreater(consts.version, (0, 0, 0))

    def test_int_to_base64(self):
        self.assertEqual(util.int_to_base64(0, 2), 'AA')
        self.assertEqual(util.int_to_base64(4095, 2), ']]')

    def test_base64_to_int(self):
        self.assertEqual(util.base64_to_int('AA'), 0)
        self.assertEqual(util.base64_to_int(']]'), 4095)
