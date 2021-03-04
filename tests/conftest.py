import datetime

import pytest
import sqlite3


@pytest.fixture
def get_stock_fake():
    stock1 = dict(
        price=531.7375,
        total=12,
        name='SBER',
        old_price=428.1,
        date=datetime.datetime.utcnow())
    stock2 = dict(
        price=531.7375,
        total=40.0,
        name='ROSN',
        old_price=428.1,
        date=datetime.datetime.utcnow())
    return [stock1, stock2]


@pytest.fixture
def setup_database_for_create():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE stock_price (
    date current_date , wealth_ratio integer, total integer, buyer_id integer, price real)
    ''')
    yield conn

