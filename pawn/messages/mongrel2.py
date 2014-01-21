from .web import WebMessage

###
### Mongrel2
###

def parse_netstring(ns):
    length, rest = ns.split(':', 1)
    length = int(length)
    assert rest[length] == ',', "Netstring did not end in ','"
    return rest[:length], rest[length + 1:]
    

class Mongrel2Message(WebMessage):
    @staticmethod
    def parse(msg):
        """Static method for constructing a Request instance out of a
        message read straight off a zmq socket.
        """
        sender, conn_id, path, rest = msg.split(' ', 3)
        headers, rest = parse_netstring(rest)
        body, _ = parse_netstring(rest)
        headers = json.loads(headers)
        # construct url from request
        scheme = headers.get('URL_SCHEME', 'http')
        netloc = headers.get('host')
        path = headers.get('PATH')
        query = headers.get('QUERY')
        url = urlparse.SplitResult(scheme, netloc, path, query, None)
        r = Mongrel2Message(sender, conn_id, path, headers, body, url)
        r.is_wsgi = False
        return r


