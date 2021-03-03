from sql_service import stock_in_db


def test_stock_in_db():
    assert stock_in_db('AFLT') is True
    assert stock_in_db('fsdfs') is False
