import unittest

from ircu import consts
from ircu import util
from ircu.util import string


class TestStringMethods(unittest.TestCase):
    def test_irc_split(self):
        cases = [
            ('PASS :muse',
             ['PASS', 'muse']),

            ('SERVER unit.test 1 1469157290 1469598599 J10 MHAD] +h6 :test',
             ['SERVER', 'unit.test', '1', '1469157290', '1469598599', 'J10',
              'MHAD]', '+h6', 'test']),

            ('MH N bc 1 1469580927 ~bc unit.test +owgrxf brian:1469589777 '
             'endurance.nasa.gov B]AAAB MHAAR :this is a test',
             ['MH', 'N', 'bc', '1', '1469580927', '~bc', 'unit.test',
              '+owgrxf', 'brian:1469589777', 'endurance.nasa.gov', 'B]AAAB',
              'MHAAR', 'this is a test']),

            ('MH EB',
             ['MH', 'EB']),
            ('MH EB ',  # ircu actually does this...
             ['MH', 'EB', '']),
        ]

        for line, splits in cases:
            self.assertEqual(splits, string.irc_split(line))

    def test_irc_buffer_lines(self):
        buf = (
            'PASS :muse\r\n'
            'SERVER unit.test 1 1468138272 1468143125 J10 F1A]] +h6 '
            ':the dream is collapsing\r\n'
            'F1 N brian 1 1468138402 ~bc 10.0.0.83 +oiwg AKAABT F1AAA :hi\r\n'
            'F1 EB \r\n')

        expected = [
            ('SERVER unit.test 1 1468138272 1468143125 J10 F1A]] +h6 '
             ':the dream is collapsing\r\n'
             'F1 N brian 1 1468138402 ~bc 10.0.0.83 +oiwg AKAABT F1AAA :hi\r\n'
             'F1 EB \r\n',
             'PASS :muse'),

            ('F1 N brian 1 1468138402 ~bc 10.0.0.83 +oiwg AKAABT F1AAA :hi\r\n'
             'F1 EB \r\n',
             'SERVER unit.test 1 1468138272 1468143125 J10 F1A]] +h6 '
             ':the dream is collapsing'),

            ('F1 EB \r\n',
             'F1 N brian 1 1468138402 ~bc 10.0.0.83 +oiwg AKAABT F1AAA :hi'),

            ('',
             'F1 EB '),
        ]

        ii = 0
        for newbuf, line in string.irc_buffer_lines(buf):
            print(ii)
            exp_newbuf, exp_line = expected[ii]
            self.assertEqual(exp_newbuf, newbuf)
            self.assertEqual(exp_line, line)
            ii += 1

        self.assertEqual(len(expected), ii)

    def test_irc_buffer_lines_incomplete(self):
        buf = (
            'PASS :muse\r\n'
            'SERVER unit.test 1 1468138272 1468143125 J10 F1A]] ')

        expected = [
            ('SERVER unit.test 1 1468138272 1468143125 J10 F1A]] ',
             'PASS :muse'),
        ]

        ii = 0
        for newbuf, line in string.irc_buffer_lines(buf):
            print(ii)
            exp_newbuf, exp_line = expected[ii]
            self.assertEqual(exp_newbuf, newbuf)
            self.assertEqual(exp_line, line)
            ii += 1

        self.assertEqual(len(expected), ii)


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
