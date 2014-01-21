def to_bytes(data, enc='utf8'):
    """Convert anything to bytes
    """
    return data.encode(enc) if isinstance(data, unicode) else bytes(data)


def to_unicode(s, enc='utf8'):
    """Convert anything to unicode
    """
    return s if isinstance(s, unicode) else unicode(str(s), encoding=enc)


class Message(object):
    """Barebones message.
    """
    def __init__(self, sender, conn_id, path, headers, body):
        self.sender = sender
        self.path = path
        self.conn_id = conn_id
        self.headers = headers
        self.body = body
        
    @staticmethod
    def parse(msg):
        return 

    def is_disconnect(self):
        return False

    def should_close(self):
        return False

    def get_arguments(self, name, strip=True):
        return None

    def get_argument(self, name, default=None, strip=True):
        return default
