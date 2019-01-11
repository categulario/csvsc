import unicodedata


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

    def target_name(self, row):
        # TODO only varify on demand
        return self.output_spec.format(*list(map(varify, row)))

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self.source)

        return {
            'data': row,
            'target': self.target_name(row),
        }
