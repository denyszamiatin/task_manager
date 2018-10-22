import pickle
import collections


class PickleSerializer:
    def __init__(self, filename='tasks.pickle'):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return collections.defaultdict(list)

    def save(self,obj):
        with open(self.filename, 'wb') as f:
            pickle.dump(obj, f)