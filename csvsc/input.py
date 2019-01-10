import os
import csv


class InputStream:

    # TODO add flags for recursive search, by default simple listing
    # TODO add flags for extensions other that csv
    def __init__(self, source):
        self.handles = []

        # TODO make the header skip a flag
        skip = 1

        if os.path.isdir(source):
            files = filter(self._allowed_file, reversed(os.listdir(source)))

            for filename in files:
                handle = open(os.path.join(source, filename))
                # TODO pass some arguments to CSV reader
                reader = csv.reader(handle)

                for i in range(skip):
                    next(reader)

                self.handles.append((handle, reader))

    def _allowed_file(self, filename):
        ext = '.csv'

        return filename.endswith(ext)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.handles) == 0:
            raise StopIteration

        while len(self.handles) > 0:
            handle, reader = self.handles[-1]

            try:
                return {
                    'data': next(reader),
                    'source': handle.name,
                }
            except StopIteration:
                handle.close()
                self.handles.pop()

        raise StopIteration
