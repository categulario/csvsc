from csvsc.distributor import Distributor


def test_distributor_target():
    d = Distributor([], '/tmp/csv/{0}_{2}.csv')

    assert d.target_name(
        ['pollo', 'verde', 'azul']
    ) == '/tmp/csv/pollo_azul.csv'


def test_distributor_varify():
    d = Distributor([], '/tmp/csv/{0}.csv')

    assert d.target_name(['póllo Verde']) == '/tmp/csv/pollo_verde.csv'
