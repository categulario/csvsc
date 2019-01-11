from csvsc.reducer import Reducer, Grouping


def test_reducer_id_function():
    r = Reducer([
        {'data': ['a'], 'target': 'a'},
        {'data': ['b'], 'target': 'a'},
        {'data': ['c'], 'target': 'a'},
    ])

    assert next(r) == {'data': ['a'], 'target': 'a'}
    assert next(r) == {'data': ['b'], 'target': 'a'}
    assert next(r) == {'data': ['c'], 'target': 'a'}


def test_reducer_avg():
    r = Reducer([
        {'data': ['1', '2'], 'target': 'a'},
        {'data': ['1', '4'], 'target': 'a'},
        {'data': ['2', '7'], 'target': 'a'},
        {'data': ['2', '9'], 'target': 'a'},
    ], grouping=Grouping('0'), columns=[Reducer.from_spec('avg:1')])

    assert next(r) == {'data': ['1', '2', '3.0'], 'target': 'a'}
    assert next(r) == {'data': ['2', '7', '8.0'], 'target': 'a'}


def test_reducer_min():
    r = Reducer([
        {'data': ['1', '2'], 'target': 'a'},
        {'data': ['1', '4'], 'target': 'a'},
        {'data': ['2', '7'], 'target': 'a'},
        {'data': ['2', '9'], 'target': 'a'},
    ], grouping=Grouping('0'), columns=[Reducer.from_spec('min:1')])

    assert next(r) == {'data': ['1', '2', '2.0'], 'target': 'a'}
    assert next(r) == {'data': ['2', '7', '7.0'], 'target': 'a'}


def test_reducer_max():
    r = Reducer([
        {'data': ['1', '2'], 'target': 'a'},
        {'data': ['1', '4'], 'target': 'a'},
        {'data': ['2', '7'], 'target': 'a'},
        {'data': ['2', '9'], 'target': 'a'},
    ], grouping=Grouping('0'), columns=[Reducer.from_spec('max:1')])

    assert next(r) == {'data': ['1', '2', '4.0'], 'target': 'a'}
    assert next(r) == {'data': ['2', '7', '9.0'], 'target': 'a'}


def test_reducer_sum():
    r = Reducer([
        {'data': ['1', '2'], 'target': 'a'},
        {'data': ['1', '4'], 'target': 'a'},
        {'data': ['2', '7'], 'target': 'a'},
        {'data': ['2', '9'], 'target': 'a'},
    ], grouping=Grouping('0'), columns=[Reducer.from_spec('sum:1')])

    assert next(r) == {'data': ['1', '2', '6.0'], 'target': 'a'}
    assert next(r) == {'data': ['2', '7', '16.0'], 'target': 'a'}
