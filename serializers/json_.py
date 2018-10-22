import json
import collections


class JsonSerializer:
    def __init__(self, filename='tasks.json'):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, 'rt') as f:
                return json.load(f, object_hook=lambda dct: collections.defaultdict(list, dct))
        except FileNotFoundError:
            return collections.defaultdict(list)

    def save(self, obj):
        with open(self.filename, 'wt') as f:
            json.dump(obj, f)