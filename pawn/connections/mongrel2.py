from .messages import (to_bytes, to_unicode, parse_netstring,
                       Mongrel2Message, WSGIMessage)
from . import concurrency
from .handlers.web import http_render

import ujson as json
from uuid import uuid4
import cgi
import re
import logging
import Cookie


def load_zmq():
    """This function exists to determine where zmq should come from and then
    cache that decision at the module level.
    """
    if not hasattr(load_zmq, '_zmq'):
        if concurrency.CORO_LIBRARY == 'gevent':
            from zmq import green as zmq
        elif concurrency.CORO_LIBRARY == 'eventlet':
            from eventlet.green import zmq
        load_zmq._zmq = zmq

    return load_zmq._zmq


def load_zmq_ctx():
    """This function exists to contain the namespace requirements of generating
    a zeromq context, while keeping the context at the module level. If other
    parts of the system need zeromq, they should use this function for access
    to the existing context.
    """
    if not hasattr(load_zmq_ctx, '_zmq_ctx'):
        zmq = load_zmq()
        zmq_ctx = zmq.Context()
        load_zmq_ctx._zmq_ctx = zmq_ctx

    return load_zmq_ctx._zmq_ctx


class Mongrel2Connection(Connection):
    """This class is an abstraction for how Brubeck sends and receives
    messages. This abstraction makes it possible for something other than
    Mongrel2 to be used easily.
    """
    MAX_IDENTS = 100

    def __init__(self, pull_addr, pub_addr):
        """sender_id = uuid.uuid4() or anything unique
        pull_addr = pull socket used for incoming messages
        pub_addr = publish socket used for outgoing messages

        The class encapsulates socket type by referring to it's pull socket
        as in_sock and it's publish socket as out_sock.
        """
        zmq = load_zmq()
        ctx = load_zmq_ctx()

        in_sock = ctx.socket(zmq.PULL)
        out_sock = ctx.socket(zmq.PUB)

        super(Mongrel2Connection, self).__init__(in_sock, out_sock)
        self.in_addr = pull_addr
        self.out_addr = pub_addr

        in_sock.connect(pull_addr)
        out_sock.setsockopt(zmq.IDENTITY, self.sender_id)
        out_sock.connect(pub_addr)

    def process_message(self, application, message):
        """This coroutine looks at the message, determines which handler will
        be used to process it, and then begins processing.

        The application is responsible for handling misconfigured routes.
        """
        request = Mongrel2Message.parse(message)
        if request.is_disconnect():
            return  # Ignore disconnect msgs. Dont have areason to do otherwise
        handler = application.route_message(request)
        result = handler()

        if result:
            http_content = http_render(result['body'], result['status_code'],
                                       result['status_msg'], result['headers'])

            application.msg_conn.reply(request, http_content)

    def recv(self):
        """Receives a raw mongrel2.handler.Request object that you from the
        zeromq socket and return whatever is found.
        """
        zmq_msg = self.in_sock.recv()
        return zmq_msg

    def recv_forever_ever(self, application):
        """Defines a function that will run the primary connection Brubeck uses
        for incoming jobs. This function should then call super which runs the
        function in a try-except that can be ctrl-c'd.
        """
        def fun_forever():
            while True:
                request = self.recv()
                concurrency.coro_spawn(self.process_message, application,
                                       request)
        self._recv_forever_ever(fun_forever)

    def send(self, uuid, conn_id, msg):
        """Raw send to the given connection ID at the given uuid, mostly used
        internally.
        """
        header = "%s %d:%s," % (uuid, len(str(conn_id)), str(conn_id))
        self.out_sock.send(header + ' ' + to_bytes(msg))

    def reply(self, req, msg):
        """Does a reply based on the given Request object and message.
        """
        self.send(req.sender, req.conn_id, msg)

    def reply_bulk(self, uuid, idents, data):
        """This lets you send a single message to many currently
        connected clients.  There's a MAX_IDENTS that you should
        not exceed, so chunk your targets as needed.  Each target
        will receive the message once by Mongrel2, but you don't have
        to loop which cuts down on reply volume.
        """
        self.send(uuid, ' '.join(idents), data)

    def close(self):
        """Tells mongrel2 to explicitly close the HTTP connection.
        """
        pass

    def close_bulk(self, uuid, idents):
        """Same as close but does it to a whole bunch of idents at a time.
        """
        self.reply_bulk(uuid, idents, "")
