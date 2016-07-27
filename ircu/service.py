import errno
import logging
import select
import socket
import time

import six

from ircu import consts
from ircu import network
from ircu import proto
from ircu import server
from ircu import util
from ircu.util import string as util_string


class SocketClosedException(Exception):
    pass


class Service(object):
    def __init__(self, conf, logger=None):
        self.conf = conf
        self.logger = logger or logging.getLogger(__name__)

        self.network = network.Network(service=self)

        self.server = server.Server(
            numeric=conf.getint('server', 'numeric'),
            name=conf.get('server', 'name'),
            info=conf.get('server', 'info'),
            max_clients=conf.getint('server', 'max_clients'),
            boot_time=time.time(),
            link_time=time.time())
        self.network.servers[self.server.num.str] = self.server
        self.uplink = None

        self.conn = None
        self.send_queue = []

        self.start_time = time.time()
        self.link_time = None

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.settimeout(self.conf.getfloat('uplink', 'timeout'))

        log_level_str = self.conf.get('logging', 'level').upper()
        if not hasattr(logging, log_level_str):
            raise ValueError('"%s" is not a valid logger level' %
                             log_level_str)

        self.logger.setLevel(getattr(logging, log_level_str))

        console_log = logging.StreamHandler()
        console_log.setFormatter(util.LogFormatter())
        self.logger.addHandler(console_log)

    def connect(self):
        self.link_time = time.time()
        return self.conn.connect((self.conf.get('uplink', 'host'),
                                  self.conf.getint('uplink', 'port')))

    def send(self, msg, *args):
        line = (msg % args)
        self.logger.debug('[SEND] %s', line)
        return self.conn.sendall(six.b(line + '\n'))

    def burst_servers(self):
        for svr_num, svr in self.network.servers.iteritems():
            if svr_num == self.server.num.str:
                continue
            self.send(consts.FMT_SERVER,
                      server.num,
                      svr.name,
                      1,
                      svr.boot_time,
                      svr.num,
                      svr.max_clients_num,
                      svr.modes or '+',
                      svr.info)

    def run(self):
        self.connect()
        self.conn.setblocking(False)

        self.send(consts.FMT_PASS, self.conf.get('uplink', 'password'))
        self.send(consts.FMT_SERVER_SELF,
                  self.server.name,
                  self.server.boot_time,
                  self.server.link_time,
                  self.server.num,
                  self.server.max_clients_num,
                  self.server.modes,
                  self.server.info)

        self.burst_servers()

        self.send(consts.FMT_ENDOFBURST, self.server.num)

        buf = ''
        while True:
            try:
                if self.send_queue:
                    for line in self.send_queue:
                        self.send(line)
                    self.send_queue = []

                ready_read, ready_write, ready_exc = select.select(
                    [self.conn], [], [], 5)

                if not ready_read:
                    continue

                try:
                    data = self.conn.recv(1024)
                except socket.error as ex:
                    self.logger.exception('Exception on socket read: [%d] %s',
                                          ex.errno, ex.strerror)
                    if ex.errno == errno.ECONNRESET:
                        raise SocketClosedException(ex)
                    elif ex.errno == errno.EAGAIN:
                        # OSX: send() on a closed socket yields EAGAIN
                        raise SocketClosedException(ex)
                    else:
                        raise

                if data == '':
                    raise SocketClosedException()

                buf += data
            except SocketClosedException:
                self.logger.warning('Socket closed, exiting')
                break

            for nextbuf, line in util_string.irc_buffer_lines(buf):
                buf = nextbuf
                self.parse(line)

    def parse(self, line):
        bits = util_string.irc_split(line)
        self.logger.debug('[RECV] %r', line)

        token = bits[1]
        num_src = bits[0]
        num_client = bits[0]
        src = None
        client = None

        if not self.uplink and bits[0][0] != ':':
            token = bits[0]
            num_src = None
            num_client = None

        if num_src:
            src = self.network.resolve_numeric(num_src)

        if num_client:
            client = self.network.resolve_numeric(num_client)

        handler_type = proto.handler_lookup(token)
        if not handler_type:
            self.logger.critical('No handler for token %s', token)
            return None

        handler = handler_type(service=self,
                               network=self.network,
                               logger=self.logger)
        handler_res = None
        if not self.uplink:
            handler_res = handler.unreg(client, src, bits[1:])
        else:
            handler_res = handler.server(client, src, bits[0:])

        if handler_res is False:
            self.logger.warning('Handler for %s returned false', token)

        return handler_res
