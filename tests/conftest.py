import datetime

import pytest


@pytest.fixture()
def get_stock():
    return dict(
        price=531.7375,
        total=40.0,
        name='ROSN',
        old_price=428.1,
        date=datetime.datetime.utcnow()
    )