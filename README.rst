ircu-python
===========

.. image:: https://travis-ci.org/briancline/ircu-python.svg?branch=master
    :target: https://travis-ci.org/briancline/ircu-python

Python library providing an Undernet-ircu network state machine and speaking
with its uplink via the P10 protocol. Provides all the plumbing necessary to
write ircu-based network services.


Requirements
------------

* Python 2.7, 3.4, or 3.5


Example Service
---------------

To create a basic service that successfully connects and watches events,
begin with the following configuration file::

    [uplink]
    host = localhost
    port = 4400
    password = s3cr3t

    [server]
    numeric = 1234
    name = service.example.com
    info = Test Service
    modes = s
    max_clients = 512

    [bot]
    nick = SpyBot
    ident = stealth
    host = example.com
    ip = 0.0.0.0
    info = Here to spy on you
    modes = owk

    [logging]
    level = DEBUG

Then, use the following code to instantiate, connect, and begin running an
event loop::

    #!/usr/bin/env python
    from ircu import service
    from ircu import util

    cfg = util.load_config('etc/example.ini')
    svc = service.Service(cfg)
    svc.run()


License
-------

This software is licensed under the MIT License. See the LICENSE file for
all the thrilling details.
