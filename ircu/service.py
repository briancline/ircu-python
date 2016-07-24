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


class SocketClosedException(Exception):
    pass


class Service(object):
    def __init__(self, conf, logger=None):
        self.conf = conf
        self.logger = logger or logging.getLogger(__name__)

        self.network = network.Network()
        self.server = server.Server(
            numeric=conf.getint('server', 'numeric'),
            name=conf.get('server', 'name'),
            info=conf.get('server', 'info'),
            max_clients=conf.getint('server', 'max_clients'))

        self.conn = None
        self.start_time = time.time()
        self.link_time = None

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.read_timeout = self.conf.getfloat('uplink', 'timeout')
        self.conn.settimeout(self.conf.getfloat('uplink', 'timeout'))

        self.logger.setLevel(logging.DEBUG)
        console_log = logging.StreamHandler()
        console_log.setFormatter(util.LogFormatter())
        self.logger.addHandler(console_log)

    def has_uplink(self):
        return len(self.network.servers) > 0

    def connect(self):
        self.link_time = time.time()
        return self.conn.connect((self.conf.get('uplink', 'host'),
                                  self.conf.getint('uplink', 'port')))

    def send(self, msg, *args):
        line = (msg % args)
        print('[SEND] %s' % line)
        return self.conn.sendall(six.b(line + '\n'))

    def run(self):
        self.connect()
        self.conn.setblocking(False)

        self.send(consts.FMT_PASS, self.conf.get('uplink', 'password'))
        self.send(consts.FMT_SERVER_SELF,
                  self.conf.get('server', 'name'),
                  self.start_time, self.link_time,
                  self.server.num,
                  util.int_to_base64(self.server.max_clients, 3),
                  self.conf.get('server', 'modes'),
                  self.server.info)

        buf = ''
        while True:
            try:
                ready_read, ready_write, ready_exc = select.select(
                    [self.conn], [], [], 5)

                if not ready_read:
                    continue

                data = self.conn.recv(1024)
                if data == '':
                    raise SocketClosedException()

                print('%r' % data)
                buf += data
            # except socket.timeout as ex:
            #     print('Socket timeout: %r: %s' % (ex.errno, ex))
            #     # if self.conn.status
            #     if ex.errno is None:
            #         continue
            #     raise
            # except socket.error as ex:
            #     print('Socket error: %r' % ex)
            #     raise
            except SocketClosedException:
                print('Socket closed, exiting')
                break

            while '\n' in buf:
                eol_idx = buf.index('\n')
                line = buf[0:eol_idx]
                buf = buf[eol_idx + 1:]
                self.parse(line)

    def parse(self, line):
        bits = util.irc_split(line)
        print('       %r' % bits)

        token = bits[1]
        num_src = bits[0]
        num_client = bits[0]
        src = None
        client = None

        if not self.has_uplink() and bits[0][0] != ':':
            token = bits[0]
            num_src = None
            num_client = None

        if num_src:
            src_len = len(num_src)
            if src_len == consts.BASE64_SERVLEN:
                src = self.network.servers.get(num_src)
            elif src_len == consts.BASE64_USERLEN:
                src = self.network.users.get(num_src)
            else:
                raise ValueError('Unknown source: %r' % num_src)

        if num_client:
            cli_len = len(num_client)
            if cli_len == consts.BASE64_SERVLEN:
                client = self.network.servers.get(num_client)
            elif cli_len == consts.BASE64_USERLEN:
                client = self.network.users.get(num_client)
            else:
                raise ValueError('Unknown client: %r' % num_client)

        handler_type = proto.handler_lookup(token)
        if not handler_type:
            self.logger.critical('No handler for token %s', token)
            return

        handler = handler_type(service=self,
                               network=self.network,
                               logger=self.logger)
        print('token %s has %s/%s handler %r' %
              (token,
               handler_type.token if handler_type else 'none',
               handler_type.command if handler_type else 'none',
               handler_type))

        res = None
        if not self.has_uplink():
            res = handler.unreg(client, src, bits[1:])
        self.logger.info('handler result=%r', res)
