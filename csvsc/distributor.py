import unicodedata
import csv


def varify(input_str):
    # https://stackoverflow.com/questions/517923
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([
        c for c in nfkd_form if not unicodedata.combining(c)
    ]).replace(' ', '_').lower()


class Distributor:

    def __init__(self, source, output_spec):
        self.source = iter(source)
        self.output_spec = output_spec
        self.targets = dict()

    def target_name(self, row):
        # TODO only varify on demand
        return self.output_spec.format(*list(map(varify, row)))

    def get_target(self, target_name):
        if target_name in self.targets:
            return self.targets[target_name][1]

        target = open(target_name, 'w')
        writer = csv.writer(target)

        self.targets[target_name] = target, writer

        return writer

    def flush(self):
        for row in self.source:
            writer = self.get_target(self.target_name(row))
            writer.writerow(row)

        for target, _ in self.targets.values():
            target.close()
