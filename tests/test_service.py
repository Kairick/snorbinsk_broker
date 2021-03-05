from service import get_stock, send_message


def test_get_stock(get_stock_fake):
    result = get_stock('ROSN', get_stock_fake)
    assert result['total'] == 40.0
    assert result['price'] == 531.7375
    assert result['name'] == "ROSN"
