from collections import OrderedDict
from uuid import uuid1
from functools import reduce
import operator


class Grouping:

    def __init__(self, columns):
        self.columns = list(map(int, columns.split(',')))

    def __call__(self, row):
        return '_'.join(map(
            lambda x: x[1],
            filter(
                lambda x: x[0] in self.columns,
                enumerate(row['data'])
            )
        )) + row['target']


class IdGrouping(Grouping):

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return str(uuid1())


class Group:

    def __init__(self, columns):
        self.columns = columns
        self.rest = None

    def update(self, row):
        if self.rest is None:
            self.rest = row

        for col in self.columns:
            col.update(row['data'])

    def row(self):
        tmp = self.rest
        tmp['data'] += [c.done() for c in self.columns]

        return tmp


class ColumnReducer:

    def __init__(self, cols):
        self.cols = cols

    def clone(self):
        return type(self)(self.cols[:])


class ReducerMax(ColumnReducer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.max = -float('inf')

    def update(self, row):
        prop = reduce(max, map(
            lambda x: float(x[1]),
            filter(
                lambda x: x[0] in self.cols,
                enumerate(row)
            )
        ), -float('inf'))

        if prop > self.max:
            self.max = prop

    def done(self):
        return str(self.max)


class ReducerMin(ColumnReducer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.min = float('inf')

    def update(self, row):
        prop = reduce(min, map(
            lambda x: float(x[1]),
            filter(
                lambda x: x[0] in self.cols,
                enumerate(row)
            )
        ), float('inf'))

        if prop < self.min:
            self.min = prop

    def done(self):
        return str(self.min)


class ReducerAvg(ColumnReducer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sum = 0
        self.total = 0

    def update(self, row):
        self.sum += reduce(operator.add, map(
            lambda x: float(x[1]),
            filter(
                lambda x: x[0] in self.cols,
                enumerate(row)
            )
        ), 0)
        self.total += len(self.cols)

    def done(self):
        if self.total == 0:
            return '#AVG_EMPTY'

        return str(self.sum / self.total)


class Reducer:

    reducers = {
        'max': ReducerMax,
        'min': ReducerMin,
        'avg': ReducerAvg,
    }

    @classmethod
    def from_spec(cls, spec):
        func, cols = spec.split(':')
        cols = list(map(int, cols.split(',')))

        return cls.reducers[func](cols)

    def __init__(self, source, grouping=None, columns=None):
        self.source = iter(source)
        self.grouping = grouping or IdGrouping()
        self.columns = columns or []
        self.groups = OrderedDict()
        self.iter_groups = None

    def _get_group(self, group_id):
        if group_id not in self.groups:
            self.groups[group_id] = Group([c.clone() for c in self.columns])

        return self.groups[group_id]

    def _proc(self):
        for row in self.source:
            group_id = self.grouping(row)

            self._get_group(group_id).update(row)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_groups is None:
            self._proc()
            self.iter_groups = iter(self.groups.values())

        return next(self.iter_groups).row()
