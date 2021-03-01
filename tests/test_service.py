from service import check_stock


def test_check_stock():
    assert check_stock('fsavfdtsfdgvsd') is None
    assert check_stock('sber') == "Сбербанк"
    assert check_stock('aflt') == "Аэрофлот"
