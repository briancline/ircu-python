from ircu import p10
from ircu import user


class MessageHandler(p10.MessageHandler):
    token = 'N'
    command = 'NICK'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def server(self, client, source, args):
        # MH N bc 1 1469568102 ~bc myhost.com +i B]AAAB MHAAQ :hi
        # MH N bc 1 1469580927 ~bc myhost.com B]AAAB MHAAR :hi
        # MH N bc 1 1469580927 ~bc myhost.com +r acct:12345678 B]AAAB MHAAR :hi
        # MH N bc 1 1469580927 ~bc myhost.com +f fake.host B]AAAB MHAAR :hi
        # MH N bc 1 1469580927 ~bc myhost +rf acct:123 aol.com B]AAAB MHAAR :hi

        modes_idx = 7
        modes = args[modes_idx] if args[modes_idx][0] == '+' else None

        account_name = None
        account_time = None
        fake_host = None

        if modes:
            # Some modes have arguments, like +r (using a registered account)
            modearg_idx = modes_idx

            if 'r' in modes:
                modearg_idx += 1
                account_name, account_time = args[modearg_idx].split(':')

            if 'f' in modes:
                modearg_idx += 1
                fake_host = args[modearg_idx]

        usr = user.User(numeric=args[-2],
                        nick=args[2],
                        ident=args[5],
                        host=args[6],
                        info=args[-1],
                        ip=args[-3],
                        modes=modes,
                        num_hops=int(args[3]),
                        connect_time=int(args[4]),
                        account_name=account_name,
                        account_time=account_time,
                        fake_host=fake_host)
        self.network.users[usr.num.str] = usr

    def client(self, client, source, args):
        self.logger.info('nick change by %s', client)
