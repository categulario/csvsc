from csvsc.reducer import Reducer, Grouping


def test_reducer_id_function():
    r = Reducer([
        ['a'],
        ['b'],
        ['c'],
    ])

    assert next(r) == ['a']
    assert next(r) == ['b']
    assert next(r) == ['c']


def test_reducer_avg():
    r = Reducer([
        ['1', '2'],
        ['1', '4'],
        ['2', '7'],
        ['2', '9'],
    ], grouping=Grouping('0'), columns=[Reducer.from_spec('avg:1')])

    assert next(r) == ['1', '2', '3.0']
    assert next(r) == ['2', '7', '8.0']


def test_reducer_min():
    r = Reducer([
        ['1', '2'],
        ['1', '4'],
        ['2', '7'],
        ['2', '9'],
    ], grouping=Grouping('0'), columns=[Reducer.from_spec('min:1')])

    assert next(r) == ['1', '2', '2.0']
    assert next(r) == ['2', '7', '7.0']


def test_reducer_max():
    r = Reducer([
        ['1', '2'],
        ['1', '4'],
        ['2', '7'],
        ['2', '9'],
    ], grouping=Grouping('0'), columns=[Reducer.from_spec('max:1')])

    assert next(r) == ['1', '2', '4.0']
    assert next(r) == ['2', '7', '9.0']
