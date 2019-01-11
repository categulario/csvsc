from csvsc.reducer import Reducer


def test_reducer_id_function():
    r = Reducer([
        ['a'],
        ['b'],
        ['c'],
    ])

    assert next(r) == ['a']
    assert next(r) == ['b']
    assert next(r) == ['c']
