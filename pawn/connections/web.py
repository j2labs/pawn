from . import to_bytes, to_unicode, Connection
from ..messages.web import WSGIMessage



###
### WSGI
###

class WSGIConnection(Connection):
    """
    """

    def __init__(self, port=6767):
        super(WSGIConnection, self).__init__()
        self.port = port

    def process_message(self, application, environ, callback):
        """Parses an incoming WSGI message and responds"""
        request = WSGIMessage.parse(environ)
        handler = application.route_message(request)
        result = handler()

        wsgi_status = ' '.join([str(result['status_code']), result['status_msg']])
        headers = [(k, v) for k,v in result['headers'].items()]
        callback(str(wsgi_status), headers)

        return [to_bytes(result['body'])]

    def recv_forever_ever(self, application):
        """Defines a function that will run the primary connection Brubeck uses
        for incoming jobs. This function should then call super which runs the
        function in a try-except that can be ctrl-c'd.
        """
        def fun_forever():
            print "Serving on port %s..." % (self.port)

            def proc_msg(environ, callback):
                return self.process_message(application, environ, callback)

            from gevent import wsgi
            server = wsgi.WSGIServer(('', self.port), proc_msg)
            server.serve_forever()

        self._recv_forever_ever(fun_forever)
