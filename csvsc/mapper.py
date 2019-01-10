import re


class ColSpec:

    def __init__(self, spec):
        if spec.startswith('regex:'):
            self.value = self._regex_value(spec)
        else:
            self.value = lambda r, s: [spec]

    def _regex_value(self, spec):
        try:
            _, source, groups, regex = spec.split(':', 3)
        except ValueError:
            raise ValueError(
                'Bad spec definition, must be regex:<source>:<groups>:<regex>'
            )

        groups = list(map(
            self._group_name,
            groups.split(',')
        ))

        def _value(d, s):
            if source == '_source':
                match = re.search(regex, s)

                if match is None:
                    return ['#RGX_MATCH_ERROR']

                res = []

                for g in groups:
                    try:
                        res.append(match.group(g))
                    except IndexError:
                        res.append('#RGX_NO_GROUP')

                return res

        return _value

    def _group_name(self, gname):
        try:
            return int(gname)
        except ValueError:
            return gname

    def __call__(self, data=None, source=None):
        return self.value(data, source)


class Mapper:

    def __init__(self, source, add_columns=None, **kwargs):
        self.source = iter(source)
        self.add_columns = add_columns if add_columns is not None else []

    def __iter__(self):
        return self

    def __next__(self):
        cur_data = next(self.source)
        data, source = cur_data['data'], cur_data['source']

        for col_spec in self.add_columns:
            data.extend(col_spec(data=data, source=source))

        return data
