from csvsc.input import InputStream
import csvsc
import os

ASSETS_DIR = os.path.normpath(os.path.join(
    os.path.dirname(csvsc.__file__),
    '../test/assets/'
))


def test_input_stream():
    inst = InputStream(os.path.join(ASSETS_DIR, 'd1/'))

    assert next(inst) == {
        'data': ['1', '30'],
        'source': '/home/abraham/src/csvsc/test/assets/d1/a1m.csv',
    }
    assert next(inst) == {
        'data': ['2', '40'],
        'source': '/home/abraham/src/csvsc/test/assets/d1/a1m.csv',
    }
    assert next(inst) == {
        'data': ['3', '20'],
        'source': '/home/abraham/src/csvsc/test/assets/d1/a2m.csv',
    }
    assert next(inst) == {
        'data': ['4', '10'],
        'source': '/home/abraham/src/csvsc/test/assets/d1/a2m.csv',
    }


def test_open_different_encoding():
    inst = InputStream(
        os.path.join(ASSETS_DIR, 'windows1252/'),
        encoding='windows-1252',
    )

    assert next(inst) == {
        'data': ['árbol'],
        'source': '/home/abraham/src/csvsc/test/assets/windows1252/data.csv',
    }
