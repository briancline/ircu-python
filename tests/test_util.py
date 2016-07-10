import unittest

from ircu import consts
from ircu import util


class TestBase64(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_int_to_base64(self):
        self.assertEqual(util.int_to_base64(0, 2), 'AA')
        self.assertEqual(util.int_to_base64(4095, 2), ']]')

    def test_base64_to_int(self):
        self.assertEqual(util.base64_to_int('AA'), 0)
        self.assertEqual(util.base64_to_int(']]'), 4095)

    def test_numeric_err_negative(self):
        with self.assertRaises(ValueError):
            util.Numeric(-5)

    def test_numeric_err_bad_type(self):
        with self.assertRaises(TypeError):
            util.Numeric(object())

    def test_numeric_err_bad_length(self):
        with self.assertRaises(ValueError):
            util.Numeric('S' * (1 + consts.BASE64_SERVLEN))
        with self.assertRaises(ValueError):
            util.UserNumeric('U' * (1 + consts.BASE64_USERLEN +
                                    consts.BASE64_SERVLEN))

    def test_numeric_server_int(self):
        n = util.Numeric(1156)
        self.assertEqual(str(n), 'SE')
        self.assertEqual(int(n), 1156)
        self.assertEqual(n.str, 'SE')
        self.assertEqual(n.int, 1156)

    def test_numeric_server_str(self):
        n = util.Numeric('SE')
        self.assertEqual(str(n), 'SE')
        self.assertEqual(n.int, 1156)

    def test_numeric_user_int(self):
        n = util.UserNumeric(236177)
        self.assertEqual(str(n), '5qR')
        self.assertEqual(n.int, 236177)

    def test_numeric_user_str(self):
        n = util.UserNumeric('5qR')
        self.assertEqual(str(n), '5qR')
        self.assertEqual(n.int, 236177)

    def test_numeric_full_int(self):
        n = util.FullNumeric(8675309)
        self.assertEqual(str(n), 'AhF]t')
        self.assertEqual(n.int, 8675309)
        self.assertEqual(str(n.server), 'Ah')
        self.assertEqual(str(n.user), 'F]t')

    def test_numeric_full_str(self):
        n = util.FullNumeric('ACBBr')
        self.assertEqual(str(n), 'ACBBr')
        self.assertEqual(n.int, 528491)
        self.assertEqual(n.server.int, 2)
        self.assertEqual(n.user.int, 4203)
