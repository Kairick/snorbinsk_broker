from unittest import TestCase

from service import check_stock, get_stock_data, prepare_stock_data


def test_check_stock():
    assert check_stock('fsavfdtsfdgvsd') is None
    assert check_stock('sber')['securities']['data'][0][2] == "Сбербанк"
    assert check_stock('aflt')['securities']['data'][0][2] == "Аэрофлот"


def test_prepare_stock_data():
    result = prepare_stock_data(get_stock_data('aflt'))
    assert result[0] == 'Аэрофлот'
    assert isinstance(result[1], float)
