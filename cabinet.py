# A very thin layer other berkeley db - it mostly serializes JSON back and forth.

import bsddb
try:
    import json
except ImportError:
    import simplejson as json


class Cabinet(object):
    def __init__(self, filename, *args):
        self.db = bsddb.hashopen(filename)
    
    def __getitem__(self, key):
        if self.db.has_key(key):
            return json.loads(self.db[key])
        else:
            raise KeyError

    def __setitem__(self, key, item):
        self.db[key] = json.dumps(item)

    def __delitem__(self, key):
        del self.db[key]

    def sync(self):
        self.db.sync()
