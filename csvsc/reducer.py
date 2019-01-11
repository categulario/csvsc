class Reducer:

    def __init__(self, source):
        self.source = iter(source)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.source)
