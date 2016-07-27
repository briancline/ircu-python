from ircu import util


class User(object):
    def __init__(self, numeric, nick, ident, host, ip, info,
                 num_hops=0, connect_time=0, modes=None, account_name=None,
                 account_time=None, fake_host=None):
        self._numeric = util.FullNumeric(numeric)
        self._nick = nick
        self._ident = ident
        self._host = host
        self._ip = util.base64_to_ip(ip)
        self._info = info

        self._modes = modes
        self._account_name = account_name
        self._account_time = account_time
        self._fake_host = fake_host

        self._connect_time = connect_time
        self._hops = num_hops

    @property
    def num(self):
        return self._numeric

    @property
    def server_num(self):
        return self._numeric.server

    @property
    def nick(self):
        return self._nick

    @property
    def ident(self):
        return self._ident

    @property
    def host(self):
        return self._host

    @property
    def fake_host(self):
        return self._fake_host

    @property
    def ip(self):
        return self._ip

    @property
    def info(self):
        return self._info

    @property
    def modes(self):
        return self._modes

    @property
    def account_name(self):
        return self._account_name

    @property
    def account_time(self):
        return self._account_time

    @property
    def connect_time(self):
        return self._connect_time

    @property
    def hops(self):
        return self._hops
