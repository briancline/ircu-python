import six

from ircu import consts
from ircu import util


class Server(object):
    def __init__(self, numeric, name, info, max_clients,
                 uplink_num=None, num_hops=0, boot_time=0, link_time=0,
                 proto=None, modes=None):
        self._numeric = util.Numeric(numeric)
        self._name = name
        self._info = info
        self._proto = proto

        self._max_clients = consts.DEFAULT_MAX_CLIENTS
        if isinstance(max_clients, six.string_types):
            self._max_clients = util.base64_to_int(max_clients)

        self._modes = modes
        self._boot_time = boot_time
        self._link_time = link_time

        self._uplink_num = None
        if uplink_num:
            self._uplink_num = util.server_num_int(uplink_num)

        self._hops = num_hops

    @property
    def num(self):
        return self._numeric

    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return self._info

    @property
    def boot_time(self):
        return self._boot_time

    @property
    def link_time(self):
        return self._link_time

    @property
    def max_clients(self):
        return self._max_clients

    @property
    def max_clients_num(self):
        return util.int_to_base64(self._max_clients, 3)

    @property
    def modes(self):
        return self._modes
