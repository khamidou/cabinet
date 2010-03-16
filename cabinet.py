# A very thin layer over berkeley db - it mostly serializes JSON back and forth.

import bsddb
try:
    import json
except ImportError:
    import simplejson as json


class Cabinet(object):
    """Persistent data storage using JSON and berkeley db"""
    def __init__(self, filename, encoder=json.JSONEncoder, decoder=None, *args):
        """Set up a Cabinet object.

        The encoder parameter is the class that will be called by the json encoder to encode python objects.
        decoder is a function which is called for each decoded object to apply special conversions.
        For more informations, see :
        http://docs.python.org/dev/library/json.html?highlight=json#encoders-and-decoders
        """
        self.db = bsddb.hashopen(filename)
        self.cache = {}
        self.encoder = encoder
        self.decoder = decoder

    def __getitem__(self, key):
        if self.cache.has_key(key):
            return self.cache[key]
        elif self.db.has_key(key):
            self.cache[key] = json.loads(self.db[key], object_hook=self.decoder)
            return self.cache[key]
        else:
            raise KeyError

    def __setitem__(self, key, item):
        self.cache[key] = item

    def __delitem__(self, key):
        del self.db[key]

    def __contains__(self, key):
        if self.cache.has_key(key):
            return True
        else:
            return False

    def sync(self):
        for key in self.cache:
            self.db[key] = json.dumps(self.cache[key], cls=self.encoder)

        self.db.sync()
