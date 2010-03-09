# A very thin layer other berkeley db - it mostly serializes JSON back and forth.

import bsddb
try:
    import json
except ImportError:
    import simplejson as json


class Cabinet(object):
    def __init__(self, filename, *args):
        self.db = bsddb.hashopen(filename)
        self.cache = {}

    def __getitem__(self, key):
        if self.cache.has_key(key):
            return self.cache[key]
        elif self.db.has_key(key):
            self.cache[key] = json.loads(self.db[key])
            return self.cache[key]
        else:
            raise KeyError

    def __setitem__(self, key, item):
        self.cache[key] = item

    def __delitem__(self, key):
        del self.db[key]

    def sync(self):
        for key in self.cache:
            self.db[key] = json.dumps(self.cache[key])

        self.db.sync()
