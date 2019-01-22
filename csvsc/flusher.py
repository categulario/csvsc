import os
import csv


class Flusher:

    def __init__(self, source):
        self.source = iter(source)
        self.targets = dict()

    def get_target(self, target_name):
        if target_name in self.targets:
            return self.targets[target_name][1]

        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(target_name), exist_ok=True)

        target = open(target_name, 'w')
        writer = csv.writer(target)

        self.targets[target_name] = target, writer

        return writer

    def flush(self):
        for row in self.source:
            writer = self.get_target(row['target'])
            writer.writerow(row['data'])

        for target, _ in self.targets.values():
            target.close()
