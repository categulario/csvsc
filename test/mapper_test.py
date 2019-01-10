import pytest

from csvsc.mapper import Mapper, ColSpec


def test_colspec_simplest():
    c = ColSpec('value')

    assert c(data=[]) == ['value']


@pytest.mark.skip
def test_colspec_incremental():
    ''' add an incremental column '''


def test_colspec_regex_source():
    c = ColSpec('regex:_source:1:a([0-9]+)m')

    assert c(data=[], source='a20m') == ['20']


def test_mapper():
    mapper = Mapper([
        {'data': ['1', '40'], 'source': '/tmp/a1m.csv'},
        {'data': ['2', '39'], 'source': '/tmp/a1m.csv'},
        {'data': ['3', '38'], 'source': '/tmp/a2m.csv'},
        {'data': ['4', '37'], 'source': '/tmp/a2m.csv'},
    ], add_columns=[ColSpec(r'regex:_source:1:a([0-9]+)m\.csv$')])

    assert next(mapper) == ['1', '40', '1']
    assert next(mapper) == ['2', '39', '1']
    assert next(mapper) == ['3', '38', '2']
    assert next(mapper) == ['4', '37', '2']
